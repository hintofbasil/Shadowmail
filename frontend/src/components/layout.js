/**
 * Layout component that queries for data
 * with Gatsby's useStaticQuery component
 *
 * See: https://www.gatsbyjs.org/docs/use-static-query/
 */

import React from 'react';
import PropTypes from 'prop-types';

import '../sass/click_me.scss';
import '../sass/descriptor.scss';
import '../sass/faq.scss';
import '../sass/footer.scss';
import '../sass/input-then-button.scss';
import '../sass/new-email-success.scss';
import '../sass/response.scss';
import '../sass/title.scss';

import './normalize.css';
import './skeleton.css';

const Layout = ({ children }) => (
  <>
      <main>{children}</main>
      <div className="footer">
        &#xa9; ShadowMail.co.uk 2017
      </div>
  </>
);

Layout.propTypes = {
  children: PropTypes.node.isRequired,
};

export default Layout;
