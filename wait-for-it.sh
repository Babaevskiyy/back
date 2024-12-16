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
                                <h6 className="text-sm font-medium text-gray-800">{selectedFile.name}</h6>
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
