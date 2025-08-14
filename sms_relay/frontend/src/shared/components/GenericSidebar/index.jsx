import './styles.less';

import NoData from '../NoData';

const GenericSidebar = ({ title, items, selectedId, onSelect, renderItem, emoji }) => {
  return (
    <div className="generic-sidebar">
      <h3 className="generic-sidebar-title">{title}</h3>
      <ul className="generic-sidebar-list">
        {items ? 
        items.map((item) => (
          <li
            key={item.id}
            className={`generic-sidebar-item${item.id === selectedId ? ' selected' : ''}`}
            onClick={() => onSelect(item)}
          >
            {renderItem(item)}
          </li>
        )) : <NoData emoji={emoji}/>}
      </ul>
    </div>
  );
};

export default GenericSidebar;
