import React, { useRef, useState, useEffect, useContext } from "react";
import axios from "axios";
import { UploadIcon, XCircleIcon, DocumentIcon } from "@heroicons/react/outline";
import { DownloadIcon } from "@heroicons/react/solid";
import SideBar from "../components/SideBar";
import AuthContext from "../contexts/AuthContext";
import Widget from "../components/Widget";

const ImportPage = () => {
    const inputRef = useRef();
    const [selectedFile, setSelectedFile] = useState(null);
    const [progress, setProgress] = useState(0);
    const [uploadStatus, setUploadStatus] = useState("select");
    const [dashboardFiles, setDashboardFiles] = useState([]);
    const [fileType, setFileType] = useState("excel");
    const [isDragActive, setIsDragActive] = useState(false);
    const [errorMessage, setErrorMessage] = useState("");
    const [rules, setRules] = useState([]);
    const [currentWidgetIndex, setCurrentWidgetIndex] = useState(0);
    const [totalProgress, setTotalProgress] = useState(0);
    const { authTokens } = useContext(AuthContext);
    const [expandedWidgets, setExpandedWidgets] = useState([]);
    const [normalizedFileUrl, setNormalizedFileUrl] = useState("");

    useEffect(() => {
        if (rules.length > 0) {
            setExpandedWidgets(rules.map((_, index) => index === 0));
        }
    }, [rules]);    
    
    useEffect(() => {
        if (uploadStatus === "done") {
            fetchNormalizationData();
        }
    }, [uploadStatus]);

    const fetchNormalizationData = async () => {
        try {
            const response = await axios.get(
                "http://185.189.14.96:8000/api/items/my-normalizations",
                {
                    headers: { Authorization: `Bearer ${authTokens.access_token}` },
                }
            );
    
            const { items } = response.data;
    
            const testData = items.map((item) => ({
                ...item,
                summary: {
                    total_names: (item.summary?.total_names || 0) + 1000, 
                    rule_1_error_count: (item.summary?.rule_1_error_count || 0) + 150,
                    rule_2_error_count: (item.summary?.rule_2_error_count || 0) + 250,
                    rule_3_error_count: (item.summary?.rule_3_error_count || 0) + 100,
                    rule_4_error_count: (item.summary?.rule_4_error_count || 0) + 300,
                    rule_5_error_count: (item.summary?.rule_5_error_count || 0) + 200,
                    rule_6_error_count: (item.summary?.rule_6_error_count || 0) + 120,
                    rule_7_error_count: (item.summary?.rule_7_error_count || 0) + 180,
                    rule_8_error_count: (item.summary?.rule_8_error_count || 0) + 90,
                    rule_9_error_count: (item.summary?.rule_9_error_count || 0) + 130,
                    rule_10_error_count: (item.summary?.rule_10_error_count || 0) + 170,
                    rule_17_error_count: (item.summary?.rule_17_error_count || 0) + 220,
                },
            }));
    
            setRules(
                testData.map((item) => ({
                    id: item.id,
                    status: item.status,
                    summary: item.summary,
                    createdAt: item.created_at,
                }))
            );
            
        } catch (error) {
            console.error("Error fetching normalization data:", error.message);
            setErrorMessage("Ошибка загрузки данных.");
        }
    };                                    

    const handleFileChange = (event) => {
        if (event.target.files && event.target.files.length > 0) {
            const file = event.target.files[0];
            if (validateFile(file)) {
                setSelectedFile(file);
                setErrorMessage("");
            }
        }
    };

    const validateFile = (file) => {
        const allowedTypes = {
            excel: ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel"],
            csv: ["text/csv"],
            json: ["application/json"],
        };

        if (!allowedTypes[fileType].includes(file.type)) {
            setErrorMessage(`Неверный формат файла. Выберите ${fileType.toUpperCase()} файл.`);
            return false;
        }
        return true;
    };

    const clearFileInput = () => {
        inputRef.current.value = "";
        setSelectedFile(null);
        setProgress(0);
        setUploadStatus("select");
        setErrorMessage("");
    };    
    
    const handleUpload = async () => {
        if (!selectedFile) return;
    
        setUploadStatus("uploading");
        setProgress(0);
    
        let currentProgress = 0;
        const fakeUpload = setInterval(() => {
            currentProgress += 20;
            if (currentProgress >= 100) {
                clearInterval(fakeUpload);
                setProgress(100);
    
                (async () => {
                    try {
                        const formData = new FormData();
                        formData.append("file", selectedFile);
                        const response = await axios.post("http://185.189.14.96:8000/api/items/upload", formData, {
                            headers: {
                                Authorization: `Bearer ${authTokens?.access_token}`,
                                "Content-Type": "multipart/form-data",
                            },
                            onUploadProgress: (progressEvent) => {
                                const percentCompleted = Math.round(
                                    (progressEvent.loaded * 100) / progressEvent.total
                                );
                                setProgress(percentCompleted);
                            },
                        });
    
                        if (response.status === 200) {
                            setDashboardFiles((prev) => [
                                ...prev,
                                {
                                    fileName: response.data.fileName || selectedFile.name,
                                    fileSize: response.data.fileSize || selectedFile.size,
                                    fileType: response.data.fileType || selectedFile.type,
                                },
                            ]);
                            setUploadStatus("done");
                        } else {
                            throw new Error("Ошибка загрузки");
                        }
                    } catch (error) {
                        console.error("Ошибка загрузки файла:", error);
                        setUploadStatus("error");
                        setErrorMessage("Ошибка загрузки файла. Попробуйте снова.");
                    }
                })();
            } else {
                setProgress(currentProgress);
            }
        }, 500); 
    };    

    const fetchNormalizedFileUrl = async (fileProcessId) => {
        try {
            const response = await axios.post(
                `http://185.189.14.96:8000/api/items/export/${fileProcessId}`,
                {},
                { headers: { Authorization: `Bearer ${authTokens.access_token}` } }
            );
            setNormalizedFileUrl(response.data.url); // Предполагается, что API возвращает URL файла
        } catch (error) {
            console.error("Ошибка получения нормализованного файла:", error.message);
        }
    };

    useEffect(() => {
        if (uploadStatus === "done" && rules.length > 0) {
            const totalProgressCompleted = rules.every(rule => rule.progress === 100);
    
            if (totalProgressCompleted) {
                fetchNormalizedFileUrl(rules[0].id); // Загрузите URL нормализованного файла
            }
        }
    }, [uploadStatus, rules]);
    

    useEffect(() => {
        if (rules.length > 0) {
            const ruleKeys = Object.keys(rules[0]?.summary || {}).filter((key) =>
                key.startsWith("rule_")
            );
    
            // Добавляем +1 для "Всего записей"
            setExpandedWidgets(new Array(ruleKeys.length + 1).fill(true));
        }
    }, [rules]);    
    
    const toggleWidget = (index) => {
        setExpandedWidgets((prev) =>
            prev.map((isOpen, i) => (i === index ? !isOpen : isOpen))
        );
    };
    
    const renderWidget = () => {
        if (rules.length === 0) {
            return <div className="text-gray-600">Данные ещё загружаются...</div>;
        }
    
        return (
            <div
                className="max-h-[80vh] overflow-y-auto w-full max-w-4xl mx-auto border border-gray-100 rounded-lg pb-8"
                style={{
                    scrollbarWidth: "none",
                    msOverflowStyle: "none",
                }}
            >
                <style>{`
                    div::-webkit-scrollbar {
                        display: none;
                    }
                `}</style>
    
                {/* Карточка для общего количества записей */}
                <Widget
                    key="total_names"
                    data={{
                        title: "Всего записей",
                        total: rules[0]?.summary?.total_names || 0,
                        progress: 100, // Для общего количества записей всегда 100%
                        isTotal: true,
                    }}
                    isExpanded={expandedWidgets[0]}
                    onToggle={() => toggleWidget(0)}
                />
    
                {/* Карточки для всех правил */}
                {Object.entries(rules[0]?.summary || {})
                    .filter(([key]) => key.startsWith("rule_")) // Фильтруем ключи
                    .map(([key, value], index) => {
                        const totalNames = rules[0]?.summary?.total_names || 1;
                        const progress = ((value || 0) / totalNames) * 100;
    
                        return (
                            <Widget
                                key={key}
                                data={{
                                    title: `Правило ${key.match(/\d+/)[0]}`,
                                    progress: progress || 0,
                                    violations: value || 0,
                                    total: totalNames,
                                }}
                                isExpanded={expandedWidgets[index + 1]}
                                onToggle={() => toggleWidget(index + 1)}
                                animationDelay={index * 200}
                            />
                        );
                    })}
            </div>
        );
    };                    
                                   

    const handleNextWidget = () => {
        setCurrentWidgetIndex((prev) => (prev + 1) % widgets.length);
    };

    const handlePreviousWidget = () => {
        setCurrentWidgetIndex((prev) => (prev - 1 + widgets.length) % widgets.length);
    };

    const widgets = rules.map((rule, index) => ({
        id: index + 1,
        title: rule.title,
        content: (
            <div className="bg-gray-50 border border-gray-100 rounded-lg p-4 flex flex-col gap-2">
                <p className="text-gray-600">{rule.description}</p>
                <div className="flex items-center gap-2">
                    <div className="relative w-full h-4 bg-gray-100 rounded-full">
                        <div
                            className="absolute top-0 left-0 h-full bg-green-500 rounded-full"
                            style={{ width: `${rule.progress}%` }}
                        ></div>
                    </div>
                    <span className="text-sm font-semibold text-green-600">{rule.progress}%</span>
                </div>
                <div className="text-sm text-gray-600">
                    {rule.current}/{rule.total} записей выполнено
                </div>
            </div>
        ),
    }));

    return (
        <div className="flex h-screen bg-gray-100">
            <SideBar isOpen={true} />
            <div className="flex-1 flex flex-col items-center bg-gray-100 justify-start mt-36 md:mt-20 px-4">
                <div className="flex gap-2 mb-2 flex-wrap">
                    <button
                        className={`px-4 py-2 rounded-md shadow-md ${
                            fileType === "excel" ? "bg-blue-600 text-white" : "bg-white text-gray-800"
                        }`}
                        onClick={() => setFileType("excel")}
                    >
                        Excel
                    </button>
                    <button
                        className={`px-4 py-2 rounded-md shadow-md ${
                            fileType === "csv" ? "bg-blue-600 text-white" : "bg-white text-gray-800"
                        }`}
                        onClick={() => setFileType("csv")}
                    >
                        CSV
                    </button>
                    <button
                        className={`px-4 py-2 rounded-md shadow-md ${
                            fileType === "json" ? "bg-blue-600 text-white" : "bg-white text-gray-800"
                        }`}
                        onClick={() => setFileType("json")}
                    >
                        JSON
                    </button>
                </div>
    
                <div
                    className={`w-full max-w-md sm:max-w-lg h-28 flex flex-col items-center justify-center gap-4 text-blue-600 rounded-lg transition mb-4 ${
                        selectedFile
                            ? "border-transparent"
                            : isDragActive
                            ? "border-4 border-blue-400 bg-blue-50 border-dashed"
                            : "border-4 border-dashed border-blue-600"
                    }`}
                    onClick={!selectedFile ? () => inputRef.current.click() : undefined}
                    onDragEnter={(e) => {
                        e.preventDefault();
                        setIsDragActive(true);
                    }}
                    onDragLeave={(e) => {
                        e.preventDefault();
                        setIsDragActive(false);
                    }}
                    onDragOver={(e) => e.preventDefault()}
                    onDrop={(e) => {
                        e.preventDefault();
                        setIsDragActive(false);
                        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
                            handleFileChange({ target: { files: e.dataTransfer.files } });
                        }
                    }}
                >
                    <input ref={inputRef} type="file" onChange={handleFileChange} className="hidden" />
                    {!selectedFile ? (
                        <>
                            <div className="w-12 h-12 bg-blue-50 rounded-full flex items-center justify-center">
                                <UploadIcon className="w-6 h-6 text-blue-600" />
                            </div>
                            {isDragActive ? (
                                <p className="text-blue-600">Отпустите файл для загрузки</p>
                            ) : (
                                <p className="text-blue-600">Перетащите файл сюда или нажмите</p>
                            )}
                        </>
                    ) : (
                        <div className="w-full h-24 flex items-center gap-4 p-4 bg-white border border-gray-200 rounded-md shadow-md">
                            <DocumentIcon className="w-8 h-8 text-blue-600" />
                            <div className="flex-1">
                                <h6 className="text-sm font-medium text-gray-800 flex items-center gap-2">
                                    {selectedFile.name}
                                    {normalizedFileUrl && (
                                        <a
                                            href={normalizedFileUrl}
                                            download
                                            className="text-blue-600 hover:underline flex items-center gap-1"
                                        >
                                            <DownloadIcon className="w-5 h-5" />
                                            Скачать
                                        </a>
                                    )}
                                </h6>
                                <div className="relative w-full h-2 bg-gray-200 rounded-md mt-2">
                                    <div
                                        className="absolute top-0 left-0 h-full bg-blue-600 rounded-md transition-all duration-500"
                                        style={{ width: `${progress}%` }}
                                    ></div>
                                </div>
                            </div>
                            <button
                                className={`w-9 h-9 rounded-full flex items-center justify-center ${
                                    uploadStatus === "uploading" ? "bg-blue-100" : "bg-blue-50"
                                }`}
                                onClick={clearFileInput}
                            >
                                {uploadStatus === "uploading" ? (
                                    <span className="text-xs font-semibold text-blue-600">{progress}%</span>
                                ) : (
                                    <XCircleIcon className="w-5 h-5 text-blue-600" />
                                )}
                            </button>
                        </div>
                    )}
                </div>
    
                {errorMessage && (
                    <div className="w-full max-w-md sm:max-w-lg text-sm text-red-600 mt-2 text-center">{errorMessage}</div>
                )}
    
                {selectedFile && uploadStatus !== "done" && (
                    <button
                        className="w-full max-w-md sm:max-w-lg px-4 py-2 bg-blue-600 text-white font-medium text-sm rounded-md shadow-md hover:bg-blue-700 mb-4"
                        onClick={handleUpload}
                    >
                        {uploadStatus === "uploading" ? "Загрузка..." : "Загрузить"}
                    </button>
                )}
    
                {uploadStatus === "done" && renderWidget()}
            </div>
        </div>
    );    
};

export default ImportPage;
