import type { ReactElement } from 'react'
import Layout from '@/components/admin/Layout'

import type { NextPageWithLayout } from './_app'
import Home from '@/components/Home'

const Page: NextPageWithLayout = () => {
  return <Home/>
}

Page.getLayout = function getLayout(page: ReactElement) {
  return (
    <Layout>
      {page}
    </Layout>
  )
}

export default Page