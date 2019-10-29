import React from 'react';

import EmailSubmitForm from '../components/email_submit_form';
import Layout from '../components/layout';
import Image from '../components/image';
import SEO from '../components/seo';

import DescriptorContainer from '../components/descriptor_container';
import FaqContainer from '../components/faq_container';

const IndexPage = () => (
  <Layout>
    <SEO title="Home" />
    <div className="body">
      <div className="container">
        <div className="row">
          <div className="offset-by-two eight columns title">
            <Image />
          </div>
        </div>
        <div className="row">
          <div className="offset-by-one ten columns sub-title">
            private email forwarding
            </div>
        </div>
        <EmailSubmitForm />
      </div>
      <DescriptorContainer />
      <FaqContainer />
    </div>
  </Layout>
);

export default IndexPage;
