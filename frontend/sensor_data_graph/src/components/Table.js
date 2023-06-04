import React from 'react';
import { DataGrid } from '@mui/x-data-grid'

function DataTable(props) {
    const { data } = props
    const columns = [
        { field: 'sensor_name', headerName: 'Sensor Name', width: 110 },
        { field: 'measurement', headerName: 'Measurement', width: 110 },
        { field: 'subsensor', headerName: 'Subsensor', width: 100 },
        { field: 'sensor_id', headerName: 'Sensor Id', width: 350 },
        { field: 'data_type_of_sensor', headerName: 'SensorData Type', width: 150 },
        { field: 'time', headerName: 'Time', width: 200 },
        { field: 'value', headerName: 'Value', width: 180 },
      ];
      
  return (
    <div style={{ height: 580, width: '100%' }}>
      <DataGrid
        rows={data}
        columns={columns}
        getRowId={(row) => row.sensor_id}
        initialState={{
          pagination: {
            paginationModel: { page: 0, pageSize: 10 },
          },
        }}
        pageSizeOptions={[ 10, 20, 50]}
        checkboxSelection
      />
    </div>
  );
}

export default DataTable;