import './styles.less';

const NoData = ({ emoji = '📭', message = 'No data found.' }) => (
  <div className="no-data">
    <div className="no-data-icon" aria-hidden="true">{emoji}</div>
    <p className="no-data-message">{message}</p>
  </div>
);

export default NoData;
