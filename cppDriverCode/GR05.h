#pragma once

#include "DeviceBase.h"

namespace kmk
{

class GR05 : public DeviceBase
{
public:
	static const int VendorId = KROMEK_VENDOR_ID;
	static const int ProductId = 0x0050;

	GR05(IDataInterface *pInterface);
	virtual ~GR05();

	virtual String GetProductName() const { return L"GR05"; }
	virtual int GetVendorID() const {return VendorId; }
	virtual int GetProductID() const {return ProductId; }

	DetectorType GetDetectorType() const { return DT_Gamma; }

	static void GetDetectorProperties(DetectorProperties &propsOut);

	String GetManufacturer() const { return L"Kromek"; }
	
};
}
