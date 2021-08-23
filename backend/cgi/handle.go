package main

import (
	"fmt"
	"net/http"

	"github.com/gin-gonic/gin"
)

type jsonBoxInfo struct {
	TypeName string `json:"TypeName" binding:"required"`
	X        int    `json:"X"`
	Y        int    `json:"Y"`
	Z        int    `json:"Z"`
	Weight   int    `json:"Weight"`
	Numbers  string `json:"Numbers"`
}

type jsonContainerInfo struct {
	ID            int    `json:"id" binding:"required"`
	X             int    `json:X`
	Y             int    `json:Y`
	Z             int    `json:Z`
	Weight_limmit int    `json:Weight_limmit`
	Numbers       string `json:"Numbers"`
}

type List struct {
	Messages []string `binding:"required"`
}

func processingJsonInfoRequest(c *gin.Context) {
	jsonData := make(map[string]interface{})
	c.BindJSON(&jsonData)
	fmt.Println("%v", &jsonData)
	c.Header("Access-Control-Allow-Origin", "*")
	c.JSON(http.StatusOK, gin.H{
		"containers": jsonData["containers"],
		"boxes":      jsonData["boxes"],
	})
}
