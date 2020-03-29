import React from "react"
import _ from 'lodash'
import { 
  useTable, 
  useSortBy, 
  usePagination, 
  useFilters, 
} from 'react-table';
import matchSorter from 'match-sorter'

import Form from 'react-bootstrap/Form'
import Popover from 'react-bootstrap/Popover';
import Tooltip from 'react-bootstrap/Tooltip';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Button from 'react-bootstrap/Button';
import Badge from 'react-bootstrap/Badge';
import Card from 'react-bootstrap/Card';

import {
  IoIosSettings, 
  IoIosLink, 
  IoIosCode, 
  IoIosMusicalNotes,
  IoMdSearch
} from "react-icons/io";
import {
  AiOutlineFullscreenExit, 
  AiOutlineFullscreen
} from 'react-icons/ai';

import { IndexTable, IndexPagination } from "../components/index-table";

// Cells

function ChecksumCell({ cell }) {
  const popover = (
    <Popover>
      <Popover.Content>
        <code className="text-muted small">{cell.value}</code>
      </Popover.Content>
    </Popover>);

  return (
    <OverlayTrigger overlay={popover} trigger="click" placement="left">
      <a className="small text-muted">{_.truncate(cell.value, {length: 5, omission: ''})}</a>
    </OverlayTrigger>
  );
}

function OptionsCell({ cell }) {
  const row = cell.row.original

  function PillLink({ children, href, ...opts}) {
    const hasHref = href !== undefined;
    const options = _.defaults(opts, {
      as: hasHref ? 'a' : 'span',
      variant: hasHref ? 'secondary' : 'light',
      href: hasHref ? href : null,
      target: '_blank'
    })
    return <Badge pill {...options}>{children}</Badge>
  }
  return (
    <>
      <PillLink className="mr-1" href={row.preview_url} title="Preview">
        <IoIosMusicalNotes />
      </PillLink>
      <PillLink className="mr-1" href={row.url} title="Go to file">
        <IoIosCode />
      </PillLink>
      <PillLink className="mr-1" href={row.source_url} title="View source document">
        <IoMdSearch />
      </PillLink>
    </>
  )
}

function TruncatedCell({ cell, maxLength, omission }) {
  maxLength = maxLength || 30
  if(typeof(cell.value) !== 'string' || cell.value.length < maxLength) {
    return cell.value
  } else {
    const tooltip = <Tooltip>{cell.value}</Tooltip>
    const truncateOptions = {length: maxLength, omission: omission || '...'}
    return (
      <OverlayTrigger placement="top" overlay={tooltip}>
        <span>{_.truncate(cell.value, truncateOptions)}</span>
      </OverlayTrigger>
    );
  }
}

function RowHeaderCell({ cell }) {
  return <strong>{cell.value}</strong>
}

function IndexOptions({ allColumns, ...opts }) {
  const popover = (
    <Popover>
      <Popover.Title>Which columns to show?</Popover.Title>
      <Popover.Content className="p-3">
        <Form style={{columns: 2}}>
          {allColumns.map(column => (
            <Form.Check
              key={column.id}
              type='checkbox'
              label={column.Header}
              {...column.getToggleHiddenProps()}
            />
          ))}
        </Form>
      </Popover.Content>
    </Popover>
  );

  return (
    <div {...opts}>
      <Button size="sm" variant="secondary" className="mr-2" disabled><AiOutlineFullscreen /></Button>
      <OverlayTrigger overlay={popover} trigger="click" placement="bottom">
        <Button size="sm" variant="secondary">Show/hide fields <IoIosSettings /></Button>
      </OverlayTrigger>
    </div>
  )
}

// Define a default UI for filtering
function DefaultColumnFilter({
  column: { filterValue, preFilteredRows, setFilter },
}) {
  const count = preFilteredRows.length

  return (
    <input
      value={filterValue || ''}
      onChange={e => {
        setFilter(e.target.value || undefined) // Set undefined to remove the filter entirely
      }}
      placeholder={`Filter...`}
      className="form-control form-control-sm"
      style={{
        height: 'calc(1rem + 0.2rem + 2px)',
        padding: '.1rem .3rem',
        fontSize: '.7rem',
        width: '100%'
      }}
    />
  )
}

function fuzzyTextFilterFn(rows, id, filterValue) {
  return matchSorter(rows, filterValue, { keys: [row => row.values[id]] })
}

// Let the table remove the filter if the string is empty
fuzzyTextFilterFn.autoRemove = val => !val

const IndeterminateCheckbox = React.forwardRef(
  ({ indeterminate, ...rest }, ref) => {
    const defaultRef = React.useRef()
    const resolvedRef = ref || defaultRef

    React.useEffect(() => {
      resolvedRef.current.indeterminate = indeterminate
    }, [resolvedRef, indeterminate])

    return <input type="checkbox" ref={resolvedRef} {...rest} />
  }
)

function Index({ columns, data, showColumns, bibliography }) {
  const defaultHiddenColumns = ['meter', 'key', 'ambitus', 'location']
  const hiddenColumns = []
  showColumns = showColumns || []
  defaultHiddenColumns.map(col => {
    if(showColumns.indexOf(col) == -1) hiddenColumns.push(col);
  })

  const filterTypes = React.useMemo(
    () => ({
      fuzzyText: fuzzyTextFilterFn,
    }),
    []
  )

  const defaultColumn = React.useMemo(() => ({
    // Let's set up our default Filter UI
    Filter: DefaultColumnFilter,
  }), [])

  const instance = useTable(
    {
      columns,
      data,
      defaultColumn,
      filterTypes,
      initialState: { 
        pageIndex: 0, 
        hiddenColumns: hiddenColumns,
        pageSize: 20 },
    },
    useFilters,
    useSortBy,
    usePagination,
  );

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    prepareRow,
    page,
    canPreviousPage,
    canNextPage,
    pageOptions,
    pageCount,
    gotoPage,
    nextPage,
    previousPage,
    setPageSize,
    allColumns,
    state,
    visibleColumns,
  } = instance;

  return (
    <Card className="w-100">
      <Card.Header>
        <div className="d-flex">
          <span>Index</span>
          <IndexOptions allColumns={allColumns} className="ml-auto" />
        </div>
      </Card.Header>
      <Card.Body>
        <IndexTable {...instance} />
      </Card.Body>
      <Card.Footer className="text-center text-muted small">
        <IndexPagination {...instance} />
      </Card.Footer>
    </Card>
  );
} 


export {
  IndexOptions,
  ChecksumCell,
  OptionsCell,
  TruncatedCell,
  RowHeaderCell,
  DefaultColumnFilter,
  IndeterminateCheckbox,
  fuzzyTextFilterFn,
  Index
}