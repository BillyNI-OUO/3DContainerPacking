package main

import (
	"net/http"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/contrib/static"
	"github.com/gin-gonic/gin"
)

func main() {

	//==============================================================
	//Gin routing table and handle request
	//==============================================================
	// Set the router as the default one shipped with Gin
	router := gin.Default()

	// Setup route group for the API
	api := router.Group("/api")
	{
		api.GET("/", func(c *gin.Context) {
			c.Header("Access-Control-Allow-Origin", "*")
			c.JSON(http.StatusOK, gin.H{
				"message": "successAccess",
			})
		})
	}

	api.POST("/ContainerAndBox/info/", processingJsonInfoRequest)
	//get rid off the CORS problem(should be fix in future)
	router.Use(cors.Default())
	router.Use(static.Serve("/", static.LocalFile("./public", true)))

	// Start and run the server
	router.Run(":4000")

}
