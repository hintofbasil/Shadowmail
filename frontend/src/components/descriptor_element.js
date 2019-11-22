import React from 'react';
import PropTypes from 'prop-types';

class DescriptorElement extends React.Component {
  render = () => (
    <div className="four columns descriptor descriptor-three">
      <div className="descriptor-title">{ this.props.title }</div>
      <div>
        <i className="material-icons descriptor-icon">{ this.props.symbol }</i>
      </div>
      <div className="descriptor-text">
        { this.props.description }
      </div>
    </div>
  )
}

DescriptorElement.propTypes = {
  title: PropTypes.string.isRequired,
  symbol: PropTypes.string.isRequired,
  description: PropTypes.string.isRequired,
};

export default DescriptorElement;
