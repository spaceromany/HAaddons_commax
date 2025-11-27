from typing import Union, Dict, Any

class StateUpdater:
    def __init__(self, ha_topic: str, publish_mqtt_func):
        self.STATE_TOPIC = ha_topic
        self.publish_mqtt = publish_mqtt_func
        # 상태 캐시: 변경된 경우에만 publish
        self._state_cache: Dict[str, Any] = {}

    def _publish_if_changed(self, topic: str, value: Any) -> bool:
        """상태가 변경된 경우에만 publish. 변경 여부 반환."""
        if self._state_cache.get(topic) == value:
            return False
        self._state_cache[topic] = value
        self.publish_mqtt(topic, value)
        return True

    def update_light_sync(self, idx: int, onoff: str) -> None:
        """동기 버전 - MQTT 콜백에서 직접 호출용"""
        state = 'power'
        deviceID = 'Light' + str(idx)
        topic = self.STATE_TOPIC.format(deviceID, state)
        self._publish_if_changed(topic, onoff)

    def update_light_breaker_sync(self, idx: int, onoff: str) -> None:
        """동기 버전 - MQTT 콜백에서 직접 호출용"""
        state = 'power'
        deviceID = 'LightBreaker' + str(idx)
        topic = self.STATE_TOPIC.format(deviceID, state)
        self._publish_if_changed(topic, onoff)

    def update_temperature_sync(self, idx: int, mode_text: str, action_text: str, curTemp: int, setTemp: int) -> None:
        """동기 버전 - MQTT 콜백에서 직접 호출용"""
        deviceID = 'Thermo' + str(idx)
        temperature = {
            'curTemp': str(curTemp).zfill(2),
            'setTemp': str(setTemp).zfill(2)
        }
        for state in temperature:
            val = temperature[state]
            topic = self.STATE_TOPIC.format(deviceID, state)
            self._publish_if_changed(topic, val)

        power_topic = self.STATE_TOPIC.format(deviceID, 'power')
        action_topic = self.STATE_TOPIC.format(deviceID, 'action')
        self._publish_if_changed(power_topic, mode_text)
        self._publish_if_changed(action_topic, action_text)

    def update_fan_sync(self, idx: int, power_text: str, speed_text: str) -> None:
        """동기 버전 - MQTT 콜백에서 직접 호출용"""
        deviceID = 'Fan' + str(idx)
        if power_text == 'OFF':
            topic = self.STATE_TOPIC.format(deviceID, 'power')
            self._publish_if_changed(topic, 'OFF')
        else:
            topic = self.STATE_TOPIC.format(deviceID, 'speed')
            self._publish_if_changed(topic, speed_text)
            topic = self.STATE_TOPIC.format(deviceID, 'power')
            self._publish_if_changed(topic, 'ON')

    def update_outlet_sync(self, idx: int, power_text: str, watt: Union[float, None],
                           cutoff: Union[int, None], is_eco: Union[bool, None]) -> None:
        """동기 버전 - MQTT 콜백에서 직접 호출용"""
        deviceID = 'Outlet' + str(idx)
        topic = self.STATE_TOPIC.format(deviceID, 'power')
        self._publish_if_changed(topic, power_text)
        if is_eco is not None:
            topic = self.STATE_TOPIC.format(deviceID, 'ecomode')
            self._publish_if_changed(topic, 'ON' if is_eco else 'OFF')
        if watt is not None:
            topic = self.STATE_TOPIC.format(deviceID, 'watt')
            self._publish_if_changed(topic, '%.1f' % watt)
        if cutoff is not None:
            topic = self.STATE_TOPIC.format(deviceID, 'cutoff')
            self._publish_if_changed(topic, str(cutoff))

    def update_gas_sync(self, idx: int, power_text: str) -> None:
        """동기 버전 - MQTT 콜백에서 직접 호출용"""
        deviceID = 'Gas' + str(idx)
        topic = self.STATE_TOPIC.format(deviceID, 'power')
        self._publish_if_changed(topic, power_text)

    def update_ev_sync(self, idx: int, power_text: str, floor_text: str) -> None:
        """동기 버전 - MQTT 콜백에서 직접 호출용"""
        deviceID = 'EV' + str(idx)
        if power_text == 'ON':
            topic = self.STATE_TOPIC.format(deviceID, 'power')
            self._publish_if_changed(topic, 'ON')
            topic = self.STATE_TOPIC.format(deviceID, 'floor')
            self._publish_if_changed(topic, floor_text)

    async def update_light(self, idx: int, onoff: str) -> None:
        state = 'power'
        deviceID = 'Light' + str(idx)

        topic = self.STATE_TOPIC.format(deviceID, state)
        self.publish_mqtt(topic, onoff)
    
    async def update_light_breaker(self, idx: int, onoff: str) -> None:
        state = 'power'
        deviceID = 'LightBreaker' + str(idx)

        topic = self.STATE_TOPIC.format(deviceID, state)
        self.publish_mqtt(topic, onoff)

    async def update_temperature(self, idx: int, mode_text: str, action_text: str, curTemp: int, setTemp: int) -> None:
        """
        온도 조절기 상태를 업데이트하는 함수입니다.

        Args:
            idx (int): 온도 조절기 장치의 인덱스 번호.
            mode_text (str): 온도 조절기의 모드 텍스트 (예: 'heat', 'off').
            action_text (str): 온도 조절기의 동작 텍스트 (예: 'heating', 'idle').
            curTemp (int): 현재 온도 값.
            setTemp (int): 설정하고자 하는 목표 온도 값.

        Raises:
            Exception: 온도 업데이트 중 오류가 발생하면 예외를 발생시킵니다.
        """
        try:
            deviceID = 'Thermo' + str(idx)
            
            # 온도 상태 업데이트
            temperature = {
                'curTemp': str(curTemp).zfill(2),
                'setTemp': str(setTemp).zfill(2)
            }
            for state in temperature:
                val = temperature[state]
                topic = self.STATE_TOPIC.format(deviceID, state)
                self.publish_mqtt(topic, val)
            
            power_topic = self.STATE_TOPIC.format(deviceID, 'power')
            action_topic = self.STATE_TOPIC.format(deviceID, 'action')
            self.publish_mqtt(power_topic, mode_text)
            self.publish_mqtt(action_topic, action_text)
            
        except Exception as e:
            raise Exception(f"온도 업데이트 중 오류 발생: {str(e)}")
 
    async def update_fan(self, idx: int, power_text: str, speed_text: str) -> None:
        try:
            deviceID = 'Fan' + str(idx)
            if power_text == 'OFF':
                topic = self.STATE_TOPIC.format(deviceID, 'power')
                self.publish_mqtt(topic,'OFF')
            else:
                topic = self.STATE_TOPIC.format(deviceID, 'speed')
                self.publish_mqtt(topic, speed_text)
                topic = self.STATE_TOPIC.format(deviceID, 'power')
                self.publish_mqtt(topic, 'ON')
                
        except Exception as e:
            raise Exception(f"팬 상태 업데이트 중 오류 발생: {str(e)}")

    async def update_outlet(self,
                            idx: int, 
                            power_text: str, 
                            watt: Union[float,None], 
                            cutoff: Union[int,None], 
                            is_eco: Union[bool,None]) -> None:
        try:
            deviceID = 'Outlet' + str(idx)
            topic = self.STATE_TOPIC.format(deviceID, 'power')
            self.publish_mqtt(topic, power_text)
            if is_eco is not None:
                topic = self.STATE_TOPIC.format(deviceID, 'ecomode')
                self.publish_mqtt(topic, 'ON' if is_eco else 'OFF')
            if watt is not None:
                topic = self.STATE_TOPIC.format(deviceID, 'watt')
                self.publish_mqtt(topic, '%.1f' % watt)
            if cutoff is not None:
                topic = self.STATE_TOPIC.format(deviceID, 'cutoff')
                self.publish_mqtt(topic, str(cutoff))

        except Exception as e:
            raise Exception(f"콘센트 상태 업데이트 중 오류 발생: {str(e)}")

    async def update_gas(self, idx: int, power_text: str) -> None:
        try:
            deviceID = 'Gas' + str(idx)
            topic = self.STATE_TOPIC.format(deviceID, 'power')
            self.publish_mqtt(topic, power_text)
        except Exception as e:
            raise Exception(f"가스밸브 상태 업데이트 중 오류 발생: {str(e)}")

    async def update_ev(self, idx: int, power_text: str, floor_text: str) -> None:
        try:
            deviceID = 'EV' + str(idx)
            if power_text == 'ON':
                topic = self.STATE_TOPIC.format(deviceID, 'power')
                self.publish_mqtt(topic, 'ON')
                topic = self.STATE_TOPIC.format(deviceID, 'floor')
                self.publish_mqtt(topic, floor_text)
        except Exception as e:
            raise Exception(f"엘리베이터 상태 업데이트 중 오류 발생: {str(e)}")