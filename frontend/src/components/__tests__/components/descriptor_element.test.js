import React from 'react';
import renderer from 'react-test-renderer';

import DescriptorELement from '../../descriptor_element';

describe('render', () => {
  it('renders successfully', () => {
    const tree = renderer
      .create(
        <DescriptorELement
          title="title"
          symbol="symbol"
          description={<span>description</span>}
        />,
      )
      .toJSON();
    expect(tree).toMatchSnapshot();
  });
});
