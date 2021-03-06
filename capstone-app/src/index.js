import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import background from './background.png';

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

var sectionStyle = {
  width: "100%",
  height: "400",
  backgroundImage: `url( ${ background })`
};

var textStyle = {
position: 'absolute',
justifyContent: 'center', 
alignItems: 'center',
top: 0,
left: 0,
right: 0,
bottom: 0
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
    alert(`Stomach pressure submitted: ${value}psi\nFlow Rate submitted: ${flowRate}ml/min`);
  }

  handleChange(event){
    this.setState({[event.target.name]:event.target.value
    })
  }

  render() {
    return (
        <form onSubmit={this.handleSubmit}>
        <section style={ sectionStyle }></section>
             <br></br>
          <div>
        <label>Enter baby stomach pressure:</label>
          <input name='value'  value={this.state.value} onChange={this.handleChange} />
          <label>psi</label>
        </div>
        <br></br>
        <br></br>
        <div>
        <label>Enter feed flow rate:</label>
          <input name='flowRate' value={this.state.flowrate} onChange={this.handleChange} />
          <label>ml/min</label>
          <br></br>
          <br></br>
        <input type="submit" value="Submit" />
        </div>
      </form>
    ); 
  }
}

ReactDOM.render(
  <FrontPage />,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
