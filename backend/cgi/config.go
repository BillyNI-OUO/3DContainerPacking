package main

import (
	"fmt"

	"github.com/spf13/viper"
)

type Configuration_struct struct {
	algorithm_package_path string
	algorithm_package_name string
	python_file_name       string
}

func printModuleHello() {
	fmt.Println("hello")
}

func getConfiguration(c *Configuration_struct) {
	viper.SetConfigName("config.json")

	// Set the path to look for the configurations file
	viper.AddConfigPath(".")

	// Enable VIPER to read Environment Variables
	viper.AutomaticEnv()

	viper.SetConfigType("json")

	if err := viper.ReadInConfig(); err != nil {
		fmt.Printf("Error reading config file, %s", err)
	}

	// Set undefined variables
	//viper.SetDefault("database.dbname", "test_db")

	err := viper.Unmarshal(c)
	if err != nil {
		fmt.Printf("Unable to decode into struct, %v", err)
	}

	fmt.Println("Reading variables using the model..")
	fmt.Printf("algorithm_package_path is %s \n", c.algorithm_package_path)
	fmt.Printf("algorithm_package_name is %s \n", c.algorithm_package_name)
	fmt.Printf("python_file_name is %s \n", c.python_file_name)

} //end getConfigureation
