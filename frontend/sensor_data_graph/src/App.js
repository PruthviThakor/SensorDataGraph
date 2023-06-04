import React, { useState, useEffect } from 'react';
import Snackbar from '@mui/material/Snackbar';
import MuiAlert from '@mui/material/Alert';
import Box from '@mui/material/Box';
import Tab from '@mui/material/Tab';
import TabContext from '@mui/lab/TabContext';
import TabList from '@mui/lab/TabList';
import TabPanel from '@mui/lab/TabPanel';
import Chart from "chart.js/auto";
import { CategoryScale } from "chart.js";
import zoomPlugin from 'chartjs-plugin-zoom';
import PieChart from './components/PieChart';
import BarChart from './components/BarChart';
import * as Utils from './components/Utils';
import './App.css';
import DataTable from './components/Table';

Chart.register(CategoryScale);
Chart.register(zoomPlugin);

const Alert = React.forwardRef(function Alert(props, ref) {
  return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});

function App() {
  const [data, setData] = useState([]);
  const [value, setValue] = useState('1');
  const [open, setOpen] = React.useState(false);


  const handleClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }

    setOpen(false);
  };

  const lineData = {
    datasets: [
      {
        label: "Dataset with string point data",
        data: data.map((value) => { return { x: Date.parse(value.time), y: value.value } }),
        backgroundColor: Utils.transparentize(Utils.CHART_COLORS.blue, 0.5),
        borderColor: Utils.CHART_COLORS.blue,
        fill: false,
      }
    ]
  };
  const [chartData, setChartData] = useState({
    labels: ["multivariate", "univariate"],
    datasets: [
      {
        label: "Sensor Data Types",
        data: [data.filter((value) => value.data_type_of_sensor === "multivariate").length, data.filter((value) => value.data_type_of_sensor === "univariate").length],
        backgroundColor: [
          "rgba(75,192,192,1)",
          "&quot;#ecf0f1",
          "#50AF95",
          "#f3ba2f",
          "#2a71d0"
        ],
        borderColor: "black",
        borderWidth: 2
      }
    ]
  });
  const [barChartData, setBarChartData] = useState(lineData)

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  const fetchData = () => {
    const headers = {
      'Access-Control-Allow-Origin': '*',
    }
    fetch(`http://127.0.0.1:5000/sensors/filter?field=value&start=-1d&end=1m`,
      {
        method: "GET",
        mode: 'cors',
        headers: headers
      })
      .then((response) => {

        if (response.status === 200) {
          return response.json()
        }
        else {
          setOpen(true);
          console.log("Something went wrong while fetching sensor data.")
          return []
        }
      })
      .then((json) => {
        setData(json);
        setBarChartData({
          datasets: [
            {
              label: "Dataset with O2 Sensor point data",
              data: json.map((value) => { return { x: Date.parse(value.time), y: value.value } }),
              backgroundColor: Utils.transparentize(Utils.CHART_COLORS.blue, 0.5),
              borderColor: Utils.CHART_COLORS.blue,
              borderWidth: 1,
              fill: false,
            }
          ]
        });
        setChartData({
          labels: ["multivariate", "univariate"],
          datasets: [
            {
              label: "Sensor Data Types",
              data: [json.filter((value) => value.data_type_of_sensor === "multivariate").length, json.filter((value) => value.data_type_of_sensor === "univariate").length],
              backgroundColor: [
                "rgba(75,192,192,1)",
                "&quot;#ecf0f1",
                "#50AF95",
                "#f3ba2f",
                "#2a71d0"
              ],
              borderColor: "black",
              borderWidth: 2
            }
          ]
        })
      });

  }

  useEffect(() => {
    fetchData()
  }, [])

  return (
    <div className="App">
      <Snackbar open={open} autoHideDuration={6000} onClose={handleClose}>
        <Alert onClose={handleClose} severity="error" sx={{ width: '100%' }}>
          Something went wrong while fetching sensor data.
        </Alert>
      </Snackbar>
      <h3>Sensor Data and Data Graphs</h3>
      <Box sx={{ width: '100%', typography: 'body1' }}>
        <TabContext value={value}>
          <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
            <TabList onChange={handleChange} aria-label="lab API tabs example">
              <Tab label="Table" value="1" />
              <Tab label="Pie Chart" value="2" />
              <Tab label="Bar chart" value="3" />
            </TabList>
          </Box>
          <TabPanel value="1"><DataTable data={data} /></TabPanel>
          <TabPanel value="2"><PieChart chartData={chartData} /></TabPanel>
          <TabPanel value="3"><BarChart chartData={barChartData} /></TabPanel>
        </TabContext>
      </Box>
    </div>
  );
}

export default App;
