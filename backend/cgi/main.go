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

type Container_struct struct {
	name      string
	x         float64
	y         float64
	z         float64
	maxWeight int
}

func embeddedPython(config *Configuration_struct) {
	python3.Py_Initialize()
	if !python3.Py_IsInitialized() {
		fmt.Println("Error initializing the python interpreter")
		os.Exit(1)
	}
	//import moulde path to embedded python
	ImportPythonModule()

	python3.PyRun_SimpleString("import sys")
	python3.PyRun_SimpleString("print(sys.path)")
	python3.PyRun_SimpleString("from py3dbp import Packer, Bin, Item")
	python3.PyRun_SimpleString("packer = Packer()")
	python3.PyRun_SimpleString("print(packer)")
	python3.PyRun_SimpleString("packer.add_bin(Bin('small-envelope', 11.5, 6.125, 0.25, 10))")
	python3.PyRun_SimpleString("packer.add_item(Item('50g [powder 1]', 3.9370, 1.9685, 1.9685, 1))")
	python3.PyRun_SimpleString("packer.pack()")
	python3.PyRun_SimpleString(`for b in packer.bins:
    print(":::::::::::", b.string())
    print("FITTED ITEMS:")
for item in b.items:
    print("====> ", item.string())

    print("UNFITTED ITEMS:")
for item in b.unfitted_items:
    print("====> ", item.string())
    `)
	//algorithm := python3.PyImport_ImportModule("py3dbp")

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
	configurations := Configuration_struct{}
	getConfiguration(&configurations)
	embeddedPython(&configurations)
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
