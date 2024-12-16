package services

import (
	"fmt"
	"strconv"

	"github.com/xuri/excelize/v2"
)

type ExportItem struct {
	Id          string `json:"id"`
	Name        string `json:"name"`
	ClearedName string `json:"cleared_name"`

	Rule1             bool   `json:"rule_1"`
	Rule2Description  string `json:"rule_2_description"`
	Rule3Description  string `json:"rule_3_description"`
	Rule4Description  string `json:"rule_4_description"`
	Rule5Description  string `json:"rule_5_description"`
	Rule6Description  string `json:"rule_6_description"`
	Rule7Description  string `json:"rule_7_description"`
	Rule8Description  string `json:"rule_8_description"`
	Rule9Description  string `json:"rule_9_description"`
	Rule10Description string `json:"rule_10_description"`
	Rule17Description string `json:"rule_17_description"`
}

func ExportItemsToXlsx(filename string, items []ExportItem) {
	f := excelize.NewFile()
	defer func() {
		if err := f.Close(); err != nil {
			fmt.Println(err)
		}
	}()

	index, err := f.NewSheet("Sheet1")
	if err != nil {
		fmt.Println(err)
		return
	}

	// TODO: Реализовать автоматическую подстановку нужной буквы
	f.SetCellValue("Sheet1", "A1", "Код")
	f.SetCellValue("Sheet1", "B1", "Наименование")
	f.SetCellValue("Sheet1", "C1", "Нормализованное наименование")
	f.SetCellValue("Sheet1", "D1", "Правило 1")
	f.SetCellValue("Sheet1", "E1", "Правило 2")
	f.SetCellValue("Sheet1", "F1", "Правило 3")
	f.SetCellValue("Sheet1", "G1", "Правило 4")
	f.SetCellValue("Sheet1", "H1", "Правило 5")
	f.SetCellValue("Sheet1", "I1", "Правило 6")
	f.SetCellValue("Sheet1", "J1", "Правило 7")
	f.SetCellValue("Sheet1", "K1", "Правило 8")
	f.SetCellValue("Sheet1", "L1", "Правило 9")
	f.SetCellValue("Sheet1", "M1", "Правило 10")
	f.SetCellValue("Sheet1", "N1", "Правило 17")
	currItem := 1
	for _, item := range items {
		currItem++
		currentItemStr := strconv.Itoa(currItem)
		f.SetCellValue("Sheet1", "A"+currentItemStr, item.Id)
		f.SetCellValue("Sheet1", "B"+currentItemStr, item.Name)
		f.SetCellValue("Sheet1", "C"+currentItemStr, item.ClearedName)
		strRule1 := "Запись нормальная"
		if !item.Rule1 {
			strRule1 = "Запись содержит ошибку"
		}
		f.SetCellValue("Sheet1", "D"+currentItemStr, strRule1)
		f.SetCellValue("Sheet1", "E"+currentItemStr, item.Rule2Description)
		f.SetCellValue("Sheet1", "F"+currentItemStr, item.Rule3Description)
		f.SetCellValue("Sheet1", "G"+currentItemStr, item.Rule4Description)
		f.SetCellValue("Sheet1", "H"+currentItemStr, item.Rule5Description)
		f.SetCellValue("Sheet1", "I"+currentItemStr, item.Rule6Description)
		f.SetCellValue("Sheet1", "J"+currentItemStr, item.Rule7Description)
		f.SetCellValue("Sheet1", "K"+currentItemStr, item.Rule8Description)
		f.SetCellValue("Sheet1", "L"+currentItemStr, item.Rule9Description)
		f.SetCellValue("Sheet1", "M"+currentItemStr, item.Rule10Description)
		f.SetCellValue("Sheet1", "N"+currentItemStr, item.Rule17Description)
	}

	f.SetColWidth("Sheet1", "A", "M", 20)

	f.SetActiveSheet(index)

	if err := f.SaveAs(filename); err != nil {
		fmt.Println(err)
	}
}
