import React from 'react';
import Layout from '../components/layout';
import SEO from '../components/seo';

import RequestDeleteForm from '../components/request_delete_form';

class RequestDelete extends React.Component {
  render = () => (
    <Layout>
      <SEO title="Home" />
      <div className="body">
        <div className="request-delete-email" />
        <div className="container">
        <RequestDeleteForm />
        </div>
      </div>
    </Layout >
  );
}

export default RequestDelete;
