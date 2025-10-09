import { Outlet, useLocation } from 'react-router-dom'

const KnowledgeLayout: React.FC = () => {
  const location = useLocation()
  console.log('KnowledgeLayout render:', location.pathname)
  return <Outlet />
}

export default KnowledgeLayout
