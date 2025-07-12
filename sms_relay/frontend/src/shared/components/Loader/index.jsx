import CircularProgress from '@mui/material/CircularProgress';
import Box from '@mui/material/Box';
import './styles.less';

const LoadingSpinner = ({ message = 'Loading...' }) => (
  <Box className="loading-spinner">
    <CircularProgress />
    {message && <div className="loading-spinner-message">{message}</div>}
  </Box>
);

export default LoadingSpinner;
