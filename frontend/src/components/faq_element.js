import React from 'react';
import PropTypes from 'prop-types';

class FaqContainer extends React.Component {
  render = () => (
    <div className="row faq-container">
      <div className="offset-by-two eight columns faq-question">
        <details>
          <summary>{ this.props.summary }</summary>
          <p>{ this.props.content }</p>
        </details>
      </div>
    </div>
  )
}

FaqContainer.propTypes = {
  summary: PropTypes.string.isRequired,
  content: PropTypes.string.isRequired,
};

export default FaqContainer;
