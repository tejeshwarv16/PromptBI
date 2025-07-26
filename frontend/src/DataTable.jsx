import React from 'react';

function DataTable({ data }) {
  if (!data || !data.columns || !data.data) {
    return null; // Don't render anything if data is not in the expected format
  }

  return (
    <table>
      <thead>
        <tr>
          {data.columns.map((column, index) => (
            <th key={index}>{column}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.data.map((row, rowIndex) => (
          <tr key={rowIndex}>
            {row.map((cell, cellIndex) => (
              <td key={cellIndex}>{cell}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default DataTable;