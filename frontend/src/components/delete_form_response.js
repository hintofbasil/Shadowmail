import React from 'react';
import PropTypes from 'prop-types';

class DeleteFormResponse extends React.Component {
  render = () => (
      <div className="row">
        <div
          className={
            this.props.status === 'OK'
              ? 'offset-by-two eight columns success-response'
              : 'offset-by-two eight columns error-response'
          }
        >
          <i className="material-icons descriptor-icon">
            {this.props.status === 'OK' ? 'mail_outline' : 'error'}
          </i>
          <br />
          {this.props.reason}
        </div>
      </div>
  )
}

DeleteFormResponse.propTypes = {
  status: PropTypes.string.isRequired,
  reason: PropTypes.string.isRequired,
};

export default DeleteFormResponse;
