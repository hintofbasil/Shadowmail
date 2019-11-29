import React from 'react';
import renderer from 'react-test-renderer';

import FaqElement from '../../faq_element';

describe('render', () => {
  it('renders successfully', () => {
    const tree = renderer
      .create(
        <FaqElement
          summary="summary"
          content="content"
        />,
      )
      .toJSON();
    expect(tree).toMatchSnapshot();
  });
});
