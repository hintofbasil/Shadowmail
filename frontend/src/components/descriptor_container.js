import React from 'react';

import DescriptorElement from './descriptor_element';

const DESCRIPTOR_CONTENT = [
  {
    title: 'Simple',
    symbol: 'done',
    description: (
      <span>
        ShadowMail is simple to use.
        Simply enter your email address and start using your
        private, virtual email address immediately.
      </span>
    ),
  },
  {
    title: 'Secure',
    symbol: 'lock',
    description: (
      <span>
        ShadowMails is 100%
        <a href="https://github.com/hintofbasil/ShadowMail"
          target="_blank"
          rel="noopener noreferrer"
        >
          open source
        </a>.
        You can audit our code yourself to ensure you&apos;re comfortable with our practises.
      </span>
    ),
  },
  {
    title: 'Private',
    symbol: 'fingerprint',
    description: (
      <span>
        We care about privacy as much as you do.  As such we never save, read or otherwise
        monitor your emails.
      </span>
    ),
  },
];

class DescriptorContainer extends React.Component {
  render = () => (
    <div className="background">
      <div className="container">
        <div className="row descriptor-container">
          {
            DESCRIPTOR_CONTENT.map(
              (element) => (
                <DescriptorElement
                  key={element.title}
                  title={element.title}
                  symbol={element.symbol}
                  description={element.description}
              />
              ),
            )
          }
        </div>
      </div>
    </div>
  )
}

export default DescriptorContainer;
