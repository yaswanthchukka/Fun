void nci_proc_prop_raw_vs_rsp(NFC_HDR* p_msg) {
    uint8_t op_code;
    tNFC_VS_CBACK* p_cback = (tNFC_VS_CBACK*)nfc_cb.p_vsc_cback;
  
    /* find the start of the NCI message and parse the NCI header */
    uint8_t* p_evt = (uint8_t*)(p_msg + 1) + p_msg->offset;
    uint8_t* p = p_evt + 1;
    NCI_MSG_PRS_HDR1(p, op_code);
  
    /* If there's a pending/stored command, restore the associated address of the
     * callback function */
    if (p_cback) {
      (*p_cback)((tNFC_VS_EVT)(NCI_RSP_BIT | op_code), p_msg->len, p_evt);
      nfc_cb.p_vsc_cback = nullptr;
    }
    nfc_cb.rawVsCbflag = false;
    nfc_ncif_update_window();
  }