package edu.mcgill.lynxiayel.androidtest;

import android.os.RemoteException;
import android.view.Surface;

import com.android.uiautomator.core.UiDevice;
import com.android.uiautomator.testrunner.UiAutomatorTestCase;

public class AndroidTest extends UiAutomatorTestCase {

	public void testChangeOrientation() throws RemoteException {
		UiDevice d = getUiDevice();
		int o = d.getDisplayRotation();
		if (o == Surface.ROTATION_0 || o == Surface.ROTATION_180)
			d.setOrientationLeft();
		else if (o == Surface.ROTATION_270 || o == Surface.ROTATION_90)
			d.setOrientationNatural();
		d.waitForIdle();
		assertEquals(o, d.getDisplayRotation());
	}

	public void testChangeRightDown() throws RemoteException {
		UiDevice d = getUiDevice();
		int o = d.getDisplayRotation();
		d.setOrientationRight();
		d.waitForIdle();
		assertEquals(o, d.getDisplayRotation());
	}

	public void testChangeLeftDown() throws RemoteException {
		UiDevice d = getUiDevice();
		int o = d.getDisplayRotation();
		d.setOrientationLeft();
		d.waitForIdle();
		assertEquals(o, d.getDisplayRotation());
	}

	public boolean testPressBack() throws RemoteException {
		UiDevice d = getUiDevice();
		return d.pressBack();
	}

	public boolean testPressHome() throws RemoteException {
		UiDevice d = getUiDevice();
		return d.pressHome();
	}

	public void testToggleScreen() throws RemoteException {
		UiDevice d = getUiDevice();
		boolean on = d.isScreenOn();
		if (on)
			d.sleep();
		else
			d.wakeUp();
		d.waitForIdle();
		assertEquals(on, d.isScreenOn());
	}

	public void testFreezeRotation() throws RemoteException {
		UiDevice d = getUiDevice();
		d.freezeRotation();
		d.waitForIdle();
	}

	public void testUnfreezeRotation() throws RemoteException {
		UiDevice d = getUiDevice();
		d.unfreezeRotation();
		d.waitForIdle();
	}

	public boolean testClick() throws RemoteException {
		UiDevice d = getUiDevice();
		int x = Integer.parseInt(getParams().getString("x"));
		int y = Integer.parseInt(getParams().getString("y"));
		return d.click(x, y);
	}

	public boolean testDrag() throws RemoteException {
		UiDevice d = getUiDevice();
		int startX = Integer.parseInt(getParams().getString("startX"));
		int startY = Integer.parseInt(getParams().getString("startY"));
		int endX = Integer.parseInt(getParams().getString("endX"));
		int endY = Integer.parseInt(getParams().getString("endY"));
		int steps = Integer.parseInt(getParams().getString("steps"));
		return d.drag(startX, startY, endX, endY, steps);
	}
}
