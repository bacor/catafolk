import React from "react"

function Name({url, children}) {
  const hasUrl = (url !== undefined) & (url !== null)
  return (
    <>
    {hasUrl
      ? <a href={url}>{children}</a>
      : <span>{children}</span> 
    }
    </>
  );
}

function Person({ name, url, role, ...options}) {
  const hasRole = (role !== undefined) & (role !== null)
  return (
    <span {...options}>
      <Name url={url}>{name}</Name>
      { hasRole ? <span className="text-muted"> ({role})</span> : null }
    </span>
  )
}

function PersonList({ persons, ...props }) {
  return (
    <div {...props}>
      {persons.map((person, i) => (
        <span key={person.name}>
          <Person name={person.name} url={person.url} role={person.role} />
          { (i < persons.length-1) ? ", " : null }
        </span>
      ))}
    </div>
  )
}

function People({ people, textProps, ...props}) {
  return (
    typeof(people) == "string"
      ? <span {...textProps} {...props}>{people}</span>
      : <PersonList persons={people} {...props} />
  )
}

export default People;
export {
  People,
  PersonList,
  Person,
  Name
}