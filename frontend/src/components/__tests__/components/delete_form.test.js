import React from 'react';
import renderer from 'react-test-renderer';

import DeleteForm from '../../delete_form';

describe('render', () => {
  it('renders successfully', () => {
    const tree = renderer
      .create(
        <DeleteForm />,
      )
      .toJSON();
    expect(tree).toMatchSnapshot();
  });
});
