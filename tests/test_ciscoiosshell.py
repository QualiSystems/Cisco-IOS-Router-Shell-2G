#!/usr/bin/env python
import unittest
from unittest.mock import patch

from cloudshell.shell.core.driver_context import ResourceCommandContext

from driver import CiscoIOSShellDriver


@patch("driver.CloudShellSessionContext")
@patch("driver.LoggingSessionContext")
@patch("driver.NetworkingResourceConfig")
@patch(
    "cloudshell.shell.core.driver_context.ResourceCommandContext",
    autospec=ResourceCommandContext,
)
@patch("driver.CiscoCli")
class TestCiscoIOSShellDriver(unittest.TestCase):
    def setUp(self):
        self.driver = CiscoIOSShellDriver()

    def test_initialize(
        self,
        mocked_cli,
        mocked_context,
        mocked_resource_details,
        mocked_logger,
        mocked_api,
    ):
        # Act
        result = self.driver.initialize(mocked_context)
        # Assert
        self.assertTrue(result, "Finished initializing")

    @patch("driver.AutoloadFlow")
    @patch("driver.NetworkingResourceModel")
    def test_get_inventory(
        self,
        mocked_resource_model,
        mocked_class,
        mocked_cli,
        mocked_context,
        mocked_resource_details,
        mocked_logger,
        mocked_api,
    ):
        # Arrange
        mocked_class.return_value.discover.return_value = ""

        # Act
        self.driver.initialize(mocked_context)
        self.driver.get_inventory(mocked_context)

        # Assert
        mocked_class.return_value.discover.assert_called()

    @patch("driver.CommandFlow")
    def test_run_custom_command(
        self,
        mocked_class,
        mocked_cli,
        mocked_context,
        mocked_resource_details,
        mocked_logger,
        mocked_api,
    ):
        # Arrange
        command = "test command"
        response = "response"
        mocked_class.return_value.run_custom_command.return_value = response

        # Act
        self.driver.initialize(mocked_context)
        result = self.driver.run_custom_command(mocked_context, command)

        # Assert
        self.assertTrue(response, result)
        mocked_class.return_value.run_custom_command.assert_called_with(
            custom_command=command
        )

    @patch("driver.StateFlow")
    def test_health_check(
        self,
        mocked_class,
        mocked_cli,
        mocked_context,
        mocked_resource_details,
        mocked_logger,
        mocked_api,
    ):
        # Arrange
        response = "response"
        mocked_class.return_value.health_check.return_value = response

        # Act
        self.driver.initialize(mocked_context)
        result = self.driver.health_check(mocked_context)

        # Assert
        self.assertTrue(response, result)
        mocked_class.return_value.health_check.assert_called_with()

    @patch("driver.CommandFlow")
    def test_run_custom_config_command(
        self,
        mocked_class,
        mocked_cli,
        mocked_context,
        mocked_resource_details,
        mocked_logger,
        mocked_api,
    ):
        # Arrange
        command = "test command"
        response = "response"
        mocked_class.return_value.run_custom_config_command.return_value = response

        # Act
        self.driver.initialize(mocked_context)
        result = self.driver.run_custom_config_command(mocked_context, command)

        # Assert
        self.assertTrue(response, result)
        mocked_class.return_value.run_custom_config_command.assert_called_with(
            custom_command=command
        )

    @patch("driver.FirmwareFlow")
    def test_load_firmware(
        self,
        mocked_class,
        mocked_cli,
        mocked_context,
        mocked_resource_details,
        mocked_logger,
        mocked_api,
    ):
        # Arrange
        path = "test"
        vrf_management_name = "response"
        mocked_class.return_value.load_firmware.return_value = ""

        # Act
        self.driver.initialize(mocked_context)
        self.driver.load_firmware(
            mocked_context, path=path, vrf_management_name=vrf_management_name
        )

        # Assert
        mocked_class.return_value.load_firmware.assert_called_with(
            path=path, vrf_management_name=vrf_management_name
        )

    @patch("driver.FirmwareFlow")
    def test_load_firmware_no_vrf(
        self,
        mocked_class,
        mocked_cli,
        mocked_context,
        mocked_resource_details,
        mocked_logger,
        mocked_api,
    ):
        # Arrange
        path = "test"
        vrf_management_name = None
        mocked_resource_details.from_context.return_value.vrf_management_name = None
        mocked_class.return_value.load_firmware.return_value = ""

        # Act
        self.driver.initialize(mocked_context)
        self.driver.load_firmware(
            context=mocked_context, path=path, vrf_management_name=vrf_management_name
        )

        # Assert
        mocked_class.return_value.load_firmware.assert_called_with(
            path=path, vrf_management_name=vrf_management_name
        )

    @patch("driver.ConfigurationFlow")
    def test_save_no_params(
        self,
        mocked_class,
        mocked_cli,
        mocked_context,
        mocked_resource_details,
        mocked_logger,
        mocked_api,
    ):
        # Arrange
        mocked_class.return_value.save.return_value = ""
        vrf_management_name = "default"
        mocked_resource_details.from_context.return_value.vrf_management_name = (
            vrf_management_name
        )

        # Act
        self.driver.initialize(mocked_context)
        self.driver.save(
            mocked_context,
            folder_path="",
            configuration_type="",
            vrf_management_name="",
        )

        # Assert
        mocked_class.return_value.save.assert_called_with(
            folder_path="",
            configuration_type="running",
            vrf_management_name=vrf_management_name,
        )

    @patch("driver.ConfigurationFlow")
    def test_save_all_params(
        self,
        mocked_class,
        mocked_cli,
        mocked_context,
        mocked_resource_details,
        mocked_logger,
        mocked_api,
    ):
        # Arrange
        folder_path = "ftp://ftpuser:ftppass@server/folder"
        configuration_type = "running"
        vrf_management_name = "vrf"

        mocked_class.return_value.save.return_value = ""

        # Act
        self.driver.initialize(mocked_context)
        self.driver.save(
            mocked_context,
            folder_path=folder_path,
            configuration_type=configuration_type,
            vrf_management_name=vrf_management_name,
        )

        # Assert
        mocked_class.return_value.save.assert_called_with(
            folder_path=folder_path,
            configuration_type=configuration_type,
            vrf_management_name=vrf_management_name,
        )

    @patch("driver.ConfigurationFlow")
    def test_save_no_vrf(
        self,
        mocked_class,
        mocked_cli,
        mocked_context,
        mocked_resource_details,
        mocked_logger,
        mocked_api,
    ):
        # Arrange
        folder_path = "ftp://ftpuser:ftppass@server/folder"
        configuration_type = "running"
        vrf = "default"
        mocked_class.return_value.save.return_value = ""
        mocked_resource_details.from_context.return_value.vrf_management_name = vrf

        # Act
        self.driver.initialize(mocked_context)
        self.driver.save(
            mocked_context,
            folder_path=folder_path,
            configuration_type=configuration_type,
            vrf_management_name=None,
        )

        # Assert
        mocked_class.return_value.save.assert_called_with(
            configuration_type=configuration_type,
            folder_path=folder_path,
            vrf_management_name=vrf,
        )

    @patch("driver.ConfigurationFlow")
    def test_save_no_vrf_no_folder_path(
        self,
        mocked_class,
        mocked_cli,
        mocked_context,
        mocked_resource_details,
        mocked_logger,
        mocked_api,
    ):
        # Arrange
        configuration_type = "running"

        vrf = "default"
        mocked_class.return_value.save.return_value = ""
        mocked_resource_details.from_context.return_value.vrf_management_name = vrf

        # Act
        self.driver.initialize(mocked_context)
        self.driver.save(
            mocked_context,
            configuration_type=configuration_type,
            folder_path="",
            vrf_management_name="",
        )

        # Assert
        mocked_class.return_value.save.assert_called_with(
            configuration_type=configuration_type,
            folder_path="",
            vrf_management_name=vrf,
        )

    @patch("driver.ConfigurationFlow")
    def test_save_no_vrf_no_config_file(
        self,
        mocked_class,
        mocked_cli,
        mocked_context,
        mocked_resource_details,
        mocked_logger,
        mocked_api,
    ):
        # Arrange
        folder_path = "ftp://ftpuser:ftppass@server/folder"
        vrf = "default"
        mocked_class.return_value.save.return_value = ""
        mocked_resource_details.from_context.return_value.vrf_management_name = vrf

        # Act
        self.driver.initialize(mocked_context)
        self.driver.save(
            mocked_context,
            folder_path=folder_path,
            configuration_type="",
            vrf_management_name="",
        )

        # Assert
        mocked_class.return_value.save.assert_called_with(
            configuration_type="running",
            folder_path=folder_path,
            vrf_management_name=vrf,
        )

    @patch("driver.ConfigurationFlow")
    def test_restore_all_params(
        self,
        mocked_class,
        mocked_cli,
        mocked_context,
        mocked_resource_details,
        mocked_logger,
        mocked_api,
    ):
        # Arrange
        path = "ftp://ftpuser:ftppass@server/folder"
        configuration_type = "startup"
        restore_method = "append"
        vrf_management_name = "vrf"
        mocked_class.return_value.restore.return_value = ""

        # Act
        self.driver.initialize(mocked_context)
        self.driver.restore(
            mocked_context,
            path=path,
            configuration_type=configuration_type,
            restore_method=restore_method,
            vrf_management_name=vrf_management_name,
        )

        # Assert
        mocked_class.return_value.restore.assert_called_with(
            path=path,
            configuration_type=configuration_type,
            restore_method=restore_method,
            vrf_management_name=vrf_management_name,
        )

    @patch("driver.ConfigurationFlow")
    def test_restore_no_vrf(
        self,
        mocked_class,
        mocked_cli,
        mocked_context,
        mocked_resource_details,
        mocked_logger,
        mocked_api,
    ):
        # Arrange
        path = "ftp://ftpuser:ftppass@server/folder"
        configuration_type = "startup"
        restore_method = "append"
        vrf = "management"
        mocked_class.return_value.restore.return_value = ""
        mocked_resource_details.from_context.return_value.vrf_management_name = vrf

        # Act
        self.driver.initialize(mocked_context)
        self.driver.restore(
            mocked_context,
            path=path,
            configuration_type=configuration_type,
            restore_method=restore_method,
            vrf_management_name="",
        )

        # Assert
        mocked_class.return_value.restore.assert_called_with(
            path=path,
            configuration_type=configuration_type,
            restore_method=restore_method,
            vrf_management_name=vrf,
        )

    @patch("driver.ConfigurationFlow")
    def test_restore_no_vrf_no_restore_method(
        self,
        mocked_class,
        mocked_cli,
        mocked_context,
        mocked_resource_details,
        mocked_logger,
        mocked_api,
    ):
        # Arrange
        path = "ftp://ftpuser:ftppass@server/folder"
        configuration_type = "startup"
        vrf = "management"
        mocked_class.return_value.restore.return_value = ""
        mocked_resource_details.from_context.return_value.vrf_management_name = vrf

        # Act
        self.driver.initialize(mocked_context)
        self.driver.restore(
            mocked_context,
            path=path,
            configuration_type=configuration_type,
            restore_method="",
            vrf_management_name="",
        )

        # Assert
        mocked_class.return_value.restore.assert_called_with(
            path=path,
            configuration_type=configuration_type,
            restore_method="override",
            vrf_management_name=vrf,
        )

    @patch("driver.ConfigurationFlow")
    def test_restore_no_optional_params(
        self,
        mocked_class,
        mocked_cli,
        mocked_context,
        mocked_resource_details,
        mocked_logger,
        mocked_api,
    ):
        # Arrange
        path = "ftp://ftpuser:ftppass@server/folder"
        mocked_class.return_value.restore.return_value = ""
        mocked_resource_details.from_context.return_value.vrf_management_name = None

        # Act
        self.driver.initialize(mocked_context)
        self.driver.restore(
            mocked_context,
            path=path,
            configuration_type=None,
            restore_method=None,
            vrf_management_name=None,
        )

        # Assert
        mocked_class.return_value.restore.assert_called_with(
            path=path,
            configuration_type="running",
            restore_method="override",
            vrf_management_name=None,
        )

    @patch("driver.ConfigurationFlow")
    @patch("driver.OrchestrationSaveRestore")
    def test_orchestration_save_no_optional_params(
        self,
        mocked_orch_service,
        mocked_class,
        mocked_cli,
        mocked_context,
        mocked_resource_details,
        mocked_logger,
        mocked_api,
    ):
        # Arrange
        save_response = "success"
        mocked_class.return_value.orchestration_save.return_value = save_response
        orch_result = mocked_orch_service.return_value.prepare_orchestration_save_result
        orch_result.return_value = ""

        # Act
        self.driver.initialize(mocked_context)
        self.driver.orchestration_save(mocked_context, None, None)

        # Assert
        orch_result.assert_called_once_with(save_response)
        mocked_class.return_value.orchestration_save.assert_called_with(
            mode="shallow", custom_params=None
        )

    @patch("driver.ConfigurationFlow")
    @patch("driver.OrchestrationSaveRestore")
    def test_orchestration_save(
        self,
        mocked_orch_service,
        mocked_class,
        mocked_cli,
        mocked_context,
        mocked_resource_details,
        mocked_logger,
        mocked_api,
    ):
        # Arrange
        mode = "shallow"
        custom_params = "test json"
        save_response = "success"
        mocked_class.return_value.orchestration_save.return_value = save_response
        orch_result = mocked_orch_service.return_value.prepare_orchestration_save_result

        orch_result.return_value = ""

        # Act
        self.driver.initialize(mocked_context)
        self.driver.orchestration_save(
            mocked_context, mode="shallow", custom_params=custom_params
        )

        # Assert
        orch_result.assert_called_once_with(save_response)
        mocked_class.return_value.orchestration_save.assert_called_with(
            mode=mode, custom_params=custom_params
        )

    @patch("driver.ConfigurationFlow")
    @patch("driver.OrchestrationSaveRestore")
    def test_orchestration_save_no_custom_params(
        self,
        mocked_orch_service,
        mocked_class,
        mocked_cli,
        mocked_context,
        mocked_resource_details,
        mocked_logger,
        mocked_api,
    ):
        # Arrange
        save_response = "success"
        mocked_class.return_value.orchestration_save.return_value = save_response
        orch_result = mocked_orch_service.return_value.prepare_orchestration_save_result
        orch_result.return_value = ""

        # Act
        self.driver.initialize(mocked_context)
        self.driver.orchestration_save(
            mocked_context, mode="shallow", custom_params=None
        )

        # Assert
        orch_result.assert_called_once_with(save_response)
        mocked_class.return_value.orchestration_save.assert_called_with(
            mode="shallow", custom_params=None
        )

    @patch("driver.ConfigurationFlow")
    @patch("driver.OrchestrationSaveRestore")
    def test_orchestration_restore_no_custom_params(
        self,
        mocked_orch_service,
        mocked_class,
        mocked_cli,
        mocked_context,
        mocked_resource_details,
        mocked_logger,
        mocked_api,
    ):
        # Arrange
        saved_artifact_info = "test json"
        custom_params = None
        mocked_class.return_value.restore.return_value = ""
        parse_result = {}
        orch_result = mocked_orch_service.return_value.parse_orchestration_save_result

        orch_result.return_value = parse_result

        # Act
        self.driver.initialize(mocked_context)
        self.driver.orchestration_restore(
            mocked_context, saved_artifact_info, custom_params
        )

        # Assert
        orch_result.assert_called_once_with(saved_artifact_info)
        mocked_class.return_value.restore.assert_called_with(**parse_result)

    @patch("driver.ConfigurationFlow")
    @patch("driver.OrchestrationSaveRestore")
    def test_orchestration_restore_all_params(
        self,
        mocked_orch_service,
        mocked_class,
        mocked_cli,
        mocked_context,
        mocked_resource_details,
        mocked_logger,
        mocked_api,
    ):
        # Arrange
        saved_artifact_info = "test json"
        custom_params = "test json"
        mocked_class.return_value.restore.return_value = ""
        parse_result = {}
        orch_result = mocked_orch_service.return_value.parse_orchestration_save_result
        orch_result.return_value = parse_result

        # Act
        self.driver.initialize(mocked_context)
        self.driver.orchestration_restore(
            mocked_context, saved_artifact_info, custom_params
        )

        # Assert

        orch_result.assert_called_once_with(saved_artifact_info)
        mocked_class.return_value.restore.assert_called_with(**parse_result)

    @patch("driver.ConnectivityFlow")
    def test_apply_connectivity_changes(
        self,
        mocked_class,
        mocked_cli,
        mocked_context,
        mocked_resource_details,
        mocked_logger,
        mocked_api,
    ):
        # Arrange
        request = "test json"
        mocked_class.return_value.apply_connectivity_changes.return_value = ""

        # Act
        self.driver.initialize(mocked_context)
        self.driver.ApplyConnectivityChanges(mocked_context, request=request)

        # Assert
        mocked_class.return_value.apply_connectivity_changes.assert_called_with(
            request=request
        )
