const h1Style = {
    textAlign: 'center',
    margin: 'auto',
    padding: '30px 0'
  };

  const h2Style = {
    textAlign: 'center',
    margin: 'auto',
    padding: '10px 0'
  };

const introFormat = (props) => {
    return (
        <div>
            <h1 style={h1Style}>
                Welcome to Homie!
            </h1>

            <h2 style={h2Style}>
                Please Login!
            </h2>
        </div>
    );
};


export default introFormat;