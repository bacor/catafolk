import React from "react"
import _ from 'lodash'

import Button from 'react-bootstrap/Button';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import ButtonToolbar from 'react-bootstrap/ButtonToolbar';
import InputGroup from 'react-bootstrap/InputGroup';
import {FaSort, FaSortUp, FaSortDown} from 'react-icons/fa';
import {Prop, PropsList} from '../components/properties'

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

function Source({author, date, title, pageNum, songNum, publisher, address, url}) {
  if(author) {
    return (
      <>
        {author ? `${author} ` : `Unknown author ` }
        {date ? `(${date}). ` : '(no date). '}
        <em>{title ? `${title}. ` : 'Unknown title. '}</em>
        {songNum && ` [${pageNum}] `}
        {pageNum && `Page ${pageNum}. `}
        {address && `${address}: `}
        {publisher && `${publisher}.`}
        {url && <a href={url}>url</a>}
      </>
    )
  } else {
    return <em className="text-muted">Unknown</em>
  }
}

function Details({row}) {
  // id
  // format
  // genre
  // has_lyrics
  // has_music
  // path
  // preview_url
  // source_key
  // title_eng
  // title
  // url
  // version
  const orig = row.original
  const opts = {
    defaultValue: <em className="text-muted">Unknown</em>,
    inRow: false
  }

  const language = `${orig.language}${orig.language_iso ? ` (${orig.language_iso})` : '' }`;

  return (
    <div className="card-deck w-100">
      <div className="card bg-light border-0">
        <div className="card-body">
          <h6 className="card-title">Collection</h6>
          <PropsList asRow={false}>
            <Prop title="Title" {...opts}>{orig.title}</Prop>
            <Prop title="Performer" {...opts}>{orig.performer}</Prop>
            <Prop title="Collector" {...opts}>{orig.collector}</Prop>
            <Prop title="Collection date" {...opts}>{orig.collection_date}</Prop>
            <Prop title="Culture" {...opts}>{orig.culture}</Prop>
            <Prop title="Location" {...opts}>{orig.location}</Prop>
            <Prop title="Latitude" {...opts}>{orig.latitude}</Prop>
            <Prop title="Longitude" {...opts}>{orig.longitude}</Prop>
          </PropsList>
        </div>
      </div>
      <div className="card bg-light border-0">
        <div className="card-body">
          <h6 className="card-title">Musical properties</h6>
          <PropsList asRow={false}>
            <Prop title="Language" {...opts}>{language}</Prop>
            <Prop title="Key" {...opts}>{orig.key}</Prop>
            <Prop title="Modality" {...opts}>{orig.modality}</Prop>
            <Prop title="Meter" {...opts}>{orig.meter}</Prop>
            <Prop title="Metric" {...opts}>{orig.metric_classification}</Prop>
            <Prop title="Ambitus" {...opts}>{orig.ambitus}</Prop>
          </PropsList>
        </div>
      </div>
      <div className="card bg-light border-0">
        <div className="card-body">
          <h6 className="card-title">Encoding</h6>
          <PropsList asRow={false}>
            <Prop title="Encoder" {...opts}>{row.original.encoder}</Prop>
            <Prop title="Encoding date" {...opts}>{row.original.encoding_date}</Prop>
            <Prop title="Source" {...opts}>
              {orig.source ? orig.source : (
                <Source 
                  author={orig.source_author}
                  title={orig.source_title}
                  date={orig.source_date}
                  pageNum={orig.source_page_num}
                  songNum={orig.source_song_num} 
                  publisher={orig.source_publisher} 
                  url={orig.source_url} />)}
            </Prop>
            <Prop title="Catalogue number" {...opts}>{orig.catalogue_num}</Prop>
            <Prop title="Copyright" {...opts}>{orig.copyright}</Prop>
            <Prop title="Checksum" {...opts}>
              <code className="text-muted">{orig.checksum}</code>
            </Prop>
          </PropsList>
        </div>
      </div>
    </div>
  )
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

function IndexTableBody({getTableBodyProps, prepareRow, page, visibleColumns}) {
  return (
    <tbody {...getTableBodyProps()}>
      {
        page.map((row, i) => {
          prepareRow(row)
          const rowProps = row.getRowProps()
          if(row.isExpanded) rowProps.className = 'bg-dark text-light';
          return (
            <React.Fragment key={rowProps.key}>  
              <tr {...rowProps}>
                {
                  row.cells.map(cell => (
                    <td {...cell.getCellProps()}>{cell.render('Cell')}</td>
                  ))
                }
              </tr>
              {/*
                  If the row is in an expanded state, render a row with a
                  column that fills the entire length of the table.
                */}
              {row.isExpanded ? (
                <tr className="bg-light text-wrap">
                  <td colSpan={visibleColumns.length}>
                    <Details row={row} />
                  </td>
                </tr>
              ) : null}
            </React.Fragment>
          )
        })
      }
    </tbody>
  )
}

function IndexTable({headerGroups, getTableBodyProps, prepareRow, page, getTableProps, visibleColumns}) {
  return (
    <table className="table table-hover text-nowrap border-top-0 table-sm small table-responsive" 
      {...getTableProps()}>
      <IndexTableHeader headerGroups={headerGroups} className="sticky-top bg-white" key="index-header" /> 
      <IndexTableBody {...{getTableBodyProps, prepareRow, page, visibleColumns }} />
    </table>
  );
}

export {
  IndexPagination,
  IndexTableHeader,
  IndexTableBody,
  IndexTable
}