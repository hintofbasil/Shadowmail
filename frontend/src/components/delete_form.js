import React from 'react';

import axios from 'axios';
import DeleteFormResponse from './delete_form_response';

const DELETE_URL = '/api/delete';

class DeleteForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      email: '',
      timestamp: '',
      token: '',
    };
  }

  componentDidMount = () => {
    const url = new URL(document.URL);
    const email = url.searchParams.get('email');
    const timestamp = url.searchParams.get('timestamp');
    const token = url.searchParams.get('token');
    this.setState({
      email,
      timestamp,
      token,
    });
  }

  handleSubmit = async (event) => {
    event.preventDefault();
    const data = {
      email: this.state.email,
      timestamp: this.state.timestamp,
      token: this.state.token,
    };
    try {
      const response = await axios.post(DELETE_URL, data);
      this.setState({
        status: response.data.status,
        reason: 'Email deleted',
      });
    } catch (error) {
      const { response } = error;
      this.setState({
        status: response.data.status || 'ERROR',
        reason: response.data.reason || 'An unexpected error occured',
      });
    }
  }

  render = () => (
    <>
        <div className="row">
          <div className="offset-by-two eight columns">
            <div className="warning1">
              Warning!
            </div>
          </div>
        </div>
        <div className="row">
          <div className="offset-by-two eight columns">
            <div className="warning2">
              This operation is not reversible.
            </div>
          </div>
        </div>
        <div className="row">
          <div className="offset-by-two eight columns">
            <form method="POST" id="click-me-form">
              <input
                type="email"
                name="email"
                id="click-me-text-input"
                placeholder="you@domain.com"
                value={this.state.email}
                readOnly
              />
              <br />
              <input
                type="submit"
                id="click-me-button"
                value="Confirm delete"
                onClick={this.handleSubmit}
              />
            </form>
          </div>
        </div>
        {this.state.status
          && <DeleteFormResponse
            status={this.state.status}
            reason={this.state.reason}
          />
        }
    </>
  )
}

export default DeleteForm;
