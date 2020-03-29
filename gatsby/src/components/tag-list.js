import React from "react"
import Badge from 'react-bootstrap/Badge';

function TagPill({ children, ...props }) {
  return <Badge pill {...props}>{children}</Badge>
}

function TagList({ tags, variant, ...props }) {
  return (
    <div {...props}>
      {tags.map(tag => (
        <TagPill variant={variant || "light"} className="mr-2" key={tag}>{tag}</TagPill>
      ))}
    </div>
  )
}

export default TagList;