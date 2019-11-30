import React from 'react';
import renderer from 'react-test-renderer';

import DescriptorContainer from '../../descriptor_container';

describe('render', () => {
  it('renders successfully', () => {
    const tree = renderer
      .create(
        <DescriptorContainer />,
      )
      .toJSON();
    expect(tree).toMatchSnapshot();
  });
});
