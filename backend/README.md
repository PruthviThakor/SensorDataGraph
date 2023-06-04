# API endpoints

These endpoints allow you to handle all influx sensor data.

## GET
 [/sensor/{sensor_id}](#get-/sensor/{sensor_id}) <br/>
 [/sensors](#get-/sensors) <br/>
 [/sensors/filter](#get-/sensors/filter) <br/>

## POST
 [/generate_data](#post-/generate_data) <br/>
[/sensor/add](#post-/sensor/add) <br/>
___

### GET /sensor/{sensor_id}
Get basics data for the given sensor ID

**Parameters**

|          Name | Required |  Type   | Description                                                                                                                                                           |
| -------------:|:--------:|:-------:| --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|     `sensor_id` | required | int  | ID of the sensor which data we require.                                                                     |


**Response**

```
[
    {"units": "ppm", "time": "06/03/2023, 18:58:50"}, 
    {"value": 770.0559628738051, "time": "06/03/2023, 18:58:50"}
]
or any implemented error
{
    "error": "An error message"
}
```
___

### GET /sensors
To get all the data for the sensor in span of year

**Parameters**

no params

**Response**

```
[
    {
        "measurement": "o2_reading",
        "units": "ppm",
        "time": "06/03/2023, 13:23:06",
        "sensor_name": "o2",
        "sensor_id": "100104044200709573019583016078813207951",
        "data_type_of_sensor": "multivariate"
    },
    .
    .
    .
    {
        "measurement": "o2_reading",
        "value": 330.5952690159193,
        "time": "06/03/2023, 13:23:06",
        "sensor_name": "o2",
        "sensor_id": "100104044200709573019583016078813207951",
        "data_type_of_sensor": "multivariate"
    },

]
or any implemented error
{
    "error": "An error message"
}
```
___

### GET /sensors/filter
To get filtered sensor data using parameters

**Parameters**

|          Name | Required |  Type   | Description                                                                                                                                                         |
| -------------:|:--------:|:-------:| ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|     `field` | optional | string  | which field to get. <br/><br/> Supported values: `value` or `units`.                                                                   |
|     `start` | optional | string  | Start time of interval. <br/><br/> Supported values ex: `-1d` or `-1h` etc.                                                                   |
|     `stop` | optional | string  | Stop time of interval. <br/><br/> Supported values ex: `1d` or `1h` etc.                                                                  |
|     `data_type_of_sensor` | optional | string  | which data type of the sensor data we want. <br/><br/> Supported values: `multivariate` or `univariate`.                                                                   |


**Response**

```
[
    {
        "measurement": "o2_reading",
        "units": "ppm",
        "time": "06/03/2023, 13:23:06",
        "sensor_name": "o2",
        "sensor_id": "100104044200709573019583016078813207951",
        "data_type_of_sensor": "multivariate"
    },
    .
    .
    .
    {
        "measurement": "o2_reading",
        "value": 330.5952690159193,
        "time": "06/03/2023, 13:23:06",
        "sensor_name": "o2",
        "sensor_id": "100104044200709573019583016078813207951",
        "data_type_of_sensor": "multivariate"
    },

]
or any implemented error
{
    "error": "An error message"
}
```
___

### POST /generate_data
Randomly generates given number of data points for Sensor

**Parameters**

|          Name | Required |   Type  | Description                                                                                                                                                         |
| -------------:|:--------:|:-------:| ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|     `number` | required | int  | number of data to generate.                                                                  |


**Response**

```
{
    "message": "data generated successfully"
}
or any implemented error
{
    "error": "An error message"
}   
```
___

### POST /sensor/add
To add custom data point to the sensor

**Body Parameters**

|          Name | Required |  Type   | Description                                                                                                                                                         |
| -------------:|:--------:|:-------:| ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|     `data_type_of_sensor` | required | string  | which data type of the sensor data we want. <br/><br/> Supported values: `multivariate` or `univariate`.            |
|    `field_value` | optional | float  | value of mesarment.    |
|     `field_units` | optional | string  | unit of the given value.    |

**Response**

```
{
    "message": "sensor 79877534771879772570964679152279527948 data added successfully"
}
or any implemented error
{
    "error": "An error message"
}
```