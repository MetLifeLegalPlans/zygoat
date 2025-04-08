import { observer } from 'mobx-react';
import PropTypes from 'prop-types';

const setDepartment = department => {
  if (typeof window === 'undefined') {
    return;
  }

  window.zESettings = {
    webWidget: {
      chat: {
        departments: {
          enabled: [department],
        },
      },
    },
  };
};

const defaultDepartment = 'Members';
import('utils/constants/chat').then(module => {
  setDepartment(module.ZENDESK_CHAT_DEPARTMENT || defaultDepartment);
});

const ChatWidget = ({ apiKey }) => {
  const widgetUrl = `https://static.zdassets.com/ekr/snippet.js?key=${apiKey}`;

  return <script id="ze-snippet" src={widgetUrl} async defer />;
};

ChatWidget.propTypes = {
  apiKey: PropTypes.string.isRequired,
};

export default observer(ChatWidget);
