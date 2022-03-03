import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);

const initialValues = {
    stomachPressure:"",
    flowrate:""
};

class FrontPage extends React.Component {
  constructor(props){
    super(props);
    this.state = {value:'', flowRate:''};
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleSubmit(event) {
    const {value, flowRate} = this.state
    event.preventDefault()
    alert(`Stomach pressure submitted: ${value}\nFlow Rate submitted: ${flowRate}`);
  }

  handleChange(event){
    // this.setState({value: event.target.value});
    this.setState({[event.target.name]:event.target.value
    })
  }



  render() {
    return (
   
        <form onSubmit={this.handleSubmit}>
             <br></br>
          <div>
        <label>Enter baby stomach pressure:</label>
          <input name='value'  value={this.state.value} onChange={this.handleChange} />
        </div>
        <br></br>
        <br></br>
        <div>
        <label>Enter feed flow rate:</label>
          {/* <input type="text" value={this.state.flowrate} onChange={this.handleChange} /> */}
          <input name='flowRate' value={this.state.flowrate} onChange={this.handleChange} />
          <br></br>
          <br></br>
        <input type="submit" value="Submit" />
        </div>
      </form>
     
    );
  }
}

// ========================================

ReactDOM.render(
  <FrontPage />,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
