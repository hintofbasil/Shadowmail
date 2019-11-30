import React from 'react';
import renderer from 'react-test-renderer';

import DeleteFormResponse from '../../delete_form_response';

describe('render', () => {
  it('renders successfully', () => {
    const tree = renderer
      .create(
        <DeleteFormResponse
          status="status"
          reason="reason"
        />,
      )
      .toJSON();
    expect(tree).toMatchSnapshot();
  });
});
