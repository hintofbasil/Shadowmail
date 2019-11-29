import React from 'react';
import renderer from 'react-test-renderer';

import EmailSubmitSuccess from '../../email_submit_success';

describe('render', () => {
  it('renders successfully', () => {
    const tree = renderer
      .create(
        <EmailSubmitSuccess
          email="test@example.com"
        />,
      )
      .toJSON();
    expect(tree).toMatchSnapshot();
  });
});
