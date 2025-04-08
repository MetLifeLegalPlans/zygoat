import { useEffect, useRef, useState } from 'react';
import PropTypes from 'prop-types';
import root from 'window-or-global';

import Modal from '@bequestinc/wui/Modal';

const activeEvents = ['mousemove', 'click', 'scroll', 'keypress'];

const IdleSessionHandler = ({ warningTime, expirationTime, expirationHandler }) => {
  const [showWarning, setShowWarning] = useState(false);
  const [expired, setExpired] = useState(false);
  const [counter, setCounter] = useState(warningTime);
  const [activeAt, setActiveAt] = useState(Date.now());
  const tickCallback = useRef();
  const resetCallback = useRef();

  useEffect(() => {
    tickCallback.current = () => {
      if (expired) {
        return;
      }
      const idleTime = Date.now() - activeAt;

      const shouldShowWarning = idleTime > warningTime;
      if (shouldShowWarning !== showWarning) {
        setShowWarning(shouldShowWarning);
      }

      if (idleTime > expirationTime) {
        expirationHandler();
        setExpired(true);
        setCounter(0);
      } else {
        setCounter(expirationTime - idleTime);
      }
    };
  }, [expirationHandler, activeAt, expired, showWarning]);

  useEffect(() => {
    resetCallback.current = () => {
      const now = Date.now();
      if (now - activeAt > 1000) {
        setActiveAt(Date.now());
        setShowWarning(false);
      }
    };
  }, [activeAt]);

  useEffect(() => {
    // The reset and tick callbacks can change while the component is mounted,
    // so we must call them using their refs.
    const resetIdleTimer = () => resetCallback.current();
    activeEvents.forEach(e => root.addEventListener(e, resetIdleTimer));
    const tickInterval = root.setInterval(() => tickCallback.current(), 1000);

    return () => {
      activeEvents.forEach(e => root.removeEventListener(e, resetIdleTimer));
      root.clearInterval(tickInterval);
    };
  }, []);

  return (
    <Modal open={showWarning} title="Expiring session due to inactivity">
      Your session will automatically expire due to inactivity in {Math.floor(counter / 1000)}{' '}
      seconds. To continue your session, press any key or move your mouse.
    </Modal>
  );
};

IdleSessionHandler.propTypes = {
  warningTime: PropTypes.number,
  expirationTime: PropTypes.number,
  expirationHandler: PropTypes.func.isRequired,
};

IdleSessionHandler.defaultProps = {
  warningTime: 25 * 60 * 1000,
  expirationTime: 30 * 60 * 1000,
};

export default IdleSessionHandler;
