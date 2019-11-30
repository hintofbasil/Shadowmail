import React from 'react';
import renderer from 'react-test-renderer';

import RequestDeleteForm from '../../request_delete_form';

describe('render', () => {
  it('renders successfully', () => {
    const tree = renderer
      .create(
        <RequestDeleteForm />,
      )
      .toJSON();
    expect(tree).toMatchSnapshot();
  });
});
