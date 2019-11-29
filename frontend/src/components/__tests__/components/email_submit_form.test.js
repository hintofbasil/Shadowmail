import React from 'react';
import renderer from 'react-test-renderer';

import EmailSubmitForm from '../../email_submit_form';

describe('render', () => {
  it('renders successfully', () => {
    const tree = renderer
      .create(
        <EmailSubmitForm />,
      )
      .toJSON();
    expect(tree).toMatchSnapshot();
  });
});
