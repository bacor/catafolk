import React from "react"
import _ from 'lodash'

import Button from 'react-bootstrap/Button';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import ButtonToolbar from 'react-bootstrap/ButtonToolbar';
import InputGroup from 'react-bootstrap/InputGroup';
import {FaSort, FaSortUp, FaSortDown} from 'react-icons/fa';


function IndexPagination({ 
    gotoPage, 
    previousPage,
    canPreviousPage,
    nextPage,
    canNextPage,
    pageCount,
    pageOptions,
    state,
    setPageSize
  }) {
  return (
    <ButtonToolbar>
      <ButtonGroup className="btn-group-sm mb-3">
        <Button variant="secondary" onClick={() => gotoPage(0)} disabled={!canPreviousPage}>
          &laquo;
        </Button>
        <Button variant="secondary" onClick={() => previousPage()} disabled={!canPreviousPage}>
          &lsaquo;
        </Button>
        <Button variant="secondary" onClick={() => nextPage()} disabled={!canNextPage}>
          &rsaquo;
        </Button>
        <Button variant="secondary" onClick={() => gotoPage(pageCount - 1)} disabled={!canNextPage}>
          &raquo;
        </Button>
      </ButtonGroup>

      <InputGroup size="sm" className="ml-2 mb-3">
        <InputGroup.Prepend>
          <InputGroup.Text>Go to page</InputGroup.Text>
        </InputGroup.Prepend>
        <input type="number"
          min="1" max={pageOptions.length}
          defaultValue={state.pageIndex + 1}
          onChange={e => {
            const page = e.target.value ? Number(e.target.value) - 1 : 0
            gotoPage(page)
          }}
          style={{ width: '50px' }}
        />
        <InputGroup.Append>
          <InputGroup.Text>of {pageOptions.length}</InputGroup.Text>
        </InputGroup.Append>
      </InputGroup>

      <InputGroup size="sm" className="ml-2 mr-2 mb-3">
        <InputGroup.Prepend>
          <InputGroup.Text>Songs per page</InputGroup.Text>
        </InputGroup.Prepend>
        <select className="custom-select custom-select-sm"
          value={state.pageSize}
          onChange={e => {setPageSize(Number(e.target.value))}}>
          {
            [10, 20, 50, 100, 200].map(pageSize => (
              <option key={pageSize} value={pageSize}>{pageSize}</option>
            ))
          }
        </select>
      </InputGroup>
    </ButtonToolbar>  
  );
}
  
function SortIcon({column}) {
  if(column.isSorted) {
    return column.isSortedDesc ? <FaSortDown /> : <FaSortUp />
  } else {
    return <FaSort />
  }
}

function IndexTableHeader({ headerGroups, className }) {
  return (
    <thead className={className}>
      {
        headerGroups.map(headerGroup => (
          <tr {...headerGroup.getHeaderGroupProps()}>
            {headerGroup.headers.map(column => (
              <th className="border-top-0 border-bottom-0 pb-1" 
                 {...column.getHeaderProps()}>
                <span {...column.getSortByToggleProps()}>{column.render('Header')}</span>
                <span className="ml-1 text-muted small" style={{ top: '-.15em', position: 'relative' }}>
                  <SortIcon column={column} />
                </span>
              </th>
            ))}
          </tr>
        ))
      }
      {
        headerGroups.map(headerGroup => (
          <tr key={`${headerGroup.getHeaderGroupProps().key}_filter`}>
            {headerGroup.headers.map(column => (
              <th className="border-top-0 pb-3" key={`header_filter_${column.id}`}>
                {column.canFilter ? column.render('Filter') : null}
              </th>
            ))}
          </tr>
        ))
      }
    </thead>
  )
}

function IndexTableBody({getTableBodyProps, prepareRow, page}) {
  return (
    <tbody {...getTableBodyProps()}>
      {
        page.map((row, i) => {
          prepareRow(row)
          return (
            <tr {...row.getRowProps()}>
              {
                row.cells.map(cell => (
                  <td {...cell.getCellProps()}>{cell.render('Cell')}</td>
                ))
              }
            </tr>
          )
        })
      }
    </tbody>
  )
}

function IndexTable({headerGroups, getTableBodyProps, prepareRow, page, getTableProps}) {
  return (
    <table className="table table-hover text-nowrap border-top-0 table-sm small table-responsive-md" 
      {...getTableProps()}>
      <IndexTableHeader headerGroups={headerGroups} className="sticky-top bg-white" key="index-header" /> 
      <IndexTableBody {...{getTableBodyProps, prepareRow, page }} />
    </table>
  );
}

export {
  IndexPagination,
  IndexTableHeader,
  IndexTableBody,
  IndexTable
}