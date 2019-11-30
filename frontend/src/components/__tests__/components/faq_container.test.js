import React from 'react';
import renderer from 'react-test-renderer';

import FaqContainer from '../../faq_container';

describe('render', () => {
  it('renders successfully', () => {
    const tree = renderer
      .create(
        <FaqContainer
          details = {[
            {
              summary: 'summary',
              content: 'content',
            },
          ]}
        />,
      )
      .toJSON();
    expect(tree).toMatchSnapshot();
  });
});
