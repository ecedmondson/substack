import { Link } from 'react-router-dom';
import './styles.less';

const Navbar = () => (
  <header className="navbar">
    <Link to="/">Home</Link>
    <Link to="/messages">Message</Link>
    {/* Add more links here */}
  </header>
);

export default Navbar;
