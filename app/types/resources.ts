interface Repository {
  id: string
  displayName: string
  url: string
  entityIds: string
  suspended: boolean
}

interface Group {
  id: string
  displayName: string
  isPublic: boolean
  joinCondition: 'open' | 'approval' | 'invite-only'
  memberVisibility: 'public' | 'private' | 'hidden'
  members?: Pick<User, 'id'>[]
}

type roleType = 'admin' | 'repoadm' | 'contributor'
interface User {
  id: string
  displayName: string
  role?: { [repo: string]: roleType }[]
  email?: string
  eppn: string
  lastModified: string
}

export type { Repository, Group, User }
