package main

import (
	"fmt"
	"net/http"
	"os"

	"github.com/DataDog/go-python3"
	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/contrib/static"
	"github.com/gin-gonic/gin"
)

func ImportPythonModule() {
	sysModule := python3.PyImport_ImportModule("sys")
	path := sysModule.GetAttrString("path")
	python3.PyList_Insert(path, 0, python3.PyUnicode_FromString(
		"/opt/share/shared_experiments/3d-bin-packing-project/3D-Binpacking-GUI/backend/algorithm/venv/lib/python3.7/site-packages/py3dbp-1.1.2-py3.7.egg"))

}

func embeddedPython() {
	python3.Py_Initialize()
	if !python3.Py_IsInitialized() {
		fmt.Println("Error initializing the python interpreter")
		os.Exit(1)
	}
	//import moulde path to embedded python
	ImportPythonModule()

	python3.PyRun_SimpleString("import sys")
	python3.PyRun_SimpleString("print(sys.path)")
	i, err := python3.PyRun_AnyFile("/opt/share/shared_experiments/3d-bin-packing-project/3D-Binpacking-GUI/backend/algorithm/example.py")
	//i, err := python3.PyRun_AnyFile("./testgopy.py")
	if err != nil {
		fmt.Printf("error launching the python interpreter: %s\n", err)
		os.Exit(1)
	}
	if i == 1 {
		fmt.Println("The interpreter exited due to an exception")
		os.Exit(1)
	}
	if i == 2 {
		fmt.Println("The parameter list does not represent a valid Python command line")
		os.Exit(1)
	}
	python3.Py_Finalize()
}
func main() {

	embeddedPython()
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
