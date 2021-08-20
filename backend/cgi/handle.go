package main

import (
	"fmt"

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

type jsonConcatedInfo struct {
	ContainerTypeNumbers int `json:"ContainerTypeNumbers"`
}

func processingJsonInfoRequest(c *gin.Context) {
	data := new(List)
	err := c.Bind(data)
	if err != nil {
		c.AbortWithError(400, err)
		return
	}
	c.String(200, fmt.Sprintf("%#v", data))
}
