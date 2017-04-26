var React = require('react');
var ReactDOM = require('react-dom');

class Shadowmail extends React.Component {
  render() {
    return <h1>Welcome to Shadowmail</h1>
  }
}

ReactDOM.render(
  React.createElement(Shadowmail),
  document.getElementById('react')
);
