import React from 'react';
import Layout from '../components/layout';
import SEO from '../components/seo';

import DeleteForm from '../components/delete_form';

class RequestDelete extends React.Component {
  render = () => (
    <Layout>
      <SEO title="Home" />
      <div className="body">
        <div className="request-delete-email" />
        <div className="container">
        <DeleteForm />
        </div>
      </div>
    </Layout >
  );
}

export default RequestDelete;
