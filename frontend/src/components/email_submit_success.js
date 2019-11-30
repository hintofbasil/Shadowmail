import React from 'react';
import PropTypes from 'prop-types';

class EmailSubmitSuccess extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      copyStatus: '',
    };
  }

  handleCopy = (event) => {
    event.preventDefault();
    const emailInput = document.getElementById('new-email-success-text');
    emailInput.select();
    const success = document.execCommand('copy');
    this.setState({
      copyStatus: success ? 'Copied!' : 'Unable to copy',
    });
  }

  render = () => (
    <>
      <div className="new-email-success-response">
        <i className="material-icons descriptor-icon">
          mail_outline
        </i>
        <br />
      </div>
      <div className="input-then-button-layout">
        <button
          type="submit"
          value="content_copy"
          title="Copy to clipboard"
          id="email-copy-button"
          onClick={this.handleCopy}
        >
          <i className="material-icons descriptor-icon submit-material-icon">
            content_copy
          </i>
          <br />
        </button>
        <span className="submit-span">
          <input type="email"
            id="new-email-success-text"
            value={this.props.email}
            readOnly
          />
        </span>
        <div id="copy-status">
          {this.state.copyStatus}
        </div>
      </div>
    </>
  );
}

EmailSubmitSuccess.propTypes = {
  email: PropTypes.string.isRequired,
};

export default EmailSubmitSuccess;
