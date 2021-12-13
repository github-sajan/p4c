


struct ethernet_t {
	bit<48> dstAddr
	bit<48> srcAddr
	bit<16> etherType
}

struct ipv4_t {
	bit<4> version
	bit<4> ihl
	bit<8> diffserv
	bit<16> totalLen
	bit<16> identification
	bit<3> flags
	bit<13> fragOffset
	bit<8> ttl
	bit<8> protocol
	bit<16> hdrChecksum
	bit<32> srcAddr
	bit<32> dstAddr
	bit<80> newfield
}

struct tcp_t {
	bit<16> srcPort
	bit<16> dstPort
	bit<32> seqNo
	bit<32> ackNo
	bit<4> dataOffset
	bit<3> res
	bit<3> ecn
	bit<6> ctrl
	bit<16> window
	bit<16> checksum
	bit<16> urgentPtr
}

struct a1_arg_t {
	bit<48> param
}

struct a2_arg_t {
	bit<16> param
}

struct user_meta_t {
	bit<32> psa_ingress_parser_input_metadata_ingress_port
	bit<32> psa_ingress_parser_input_metadata_packet_path
	bit<32> psa_egress_parser_input_metadata_egress_port
	bit<32> psa_egress_parser_input_metadata_packet_path
	bit<32> psa_ingress_input_metadata_ingress_port
	bit<32> psa_ingress_input_metadata_packet_path
	bit<64> psa_ingress_input_metadata_ingress_timestamp
	bit<8> psa_ingress_input_metadata_parser_error
	bit<8> psa_ingress_output_metadata_class_of_service
	bit<8> psa_ingress_output_metadata_clone
	bit<16> psa_ingress_output_metadata_clone_session_id
	bit<8> psa_ingress_output_metadata_drop
	bit<8> psa_ingress_output_metadata_resubmit
	bit<32> psa_ingress_output_metadata_multicast_group
	bit<32> psa_ingress_output_metadata_egress_port
	bit<8> psa_egress_input_metadata_class_of_service
	bit<32> psa_egress_input_metadata_egress_port
	bit<32> psa_egress_input_metadata_packet_path
	bit<16> psa_egress_input_metadata_instance
	bit<64> psa_egress_input_metadata_egress_timestamp
	bit<8> psa_egress_input_metadata_parser_error
	bit<32> psa_egress_deparser_input_metadata_egress_port
	bit<8> psa_egress_output_metadata_clone
	bit<16> psa_egress_output_metadata_clone_session_id
	bit<8> psa_egress_output_metadata_drop
	bit<16> local_metadata_data
	bit<16> local_metadata_data1
	bit<16> Ingress_tmp_0
	bit<16> Ingress_switch_0_key
	bit<48> Ingress_tbl_ethernet_srcAddr
	bit<16> tmpMask
	bit<8> tmpMask_0
}
metadata instanceof user_meta_t

header ethernet instanceof ethernet_t
header ipv4 instanceof ipv4_t
header tcp instanceof tcp_t

struct psa_ingress_output_metadata_t {
	bit<8> class_of_service
	bit<8> clone
	bit<16> clone_session_id
	bit<8> drop
	bit<8> resubmit
	bit<32> multicast_group
	bit<32> egress_port
}

struct psa_egress_output_metadata_t {
	bit<8> clone
	bit<16> clone_session_id
	bit<8> drop
}

struct psa_egress_deparser_input_metadata_t {
	bit<32> egress_port
}

action NoAction args none {
	return
}

action a1 args instanceof a1_arg_t {
	mov h.ethernet.dstAddr t.param
	return
}

action a2 args instanceof a2_arg_t {
	mov h.ethernet.etherType t.param
	return
}

action switch_0_case args none {
	return
}

action switch_0_case_0 args none {
	return
}

action switch_0_case_1 args none {
	return
}

table tbl {
	key {
		m.Ingress_tbl_ethernet_srcAddr exact
		m.local_metadata_data lpm
	}
	actions {
		NoAction
		a1
		a2
	}
	default_action NoAction args none 
	size 0x10000
}


table foo {
	actions {
		NoAction
	}
	default_action NoAction args none 
	size 0x10000
}


table bar {
	actions {
		NoAction
	}
	default_action NoAction args none 
	size 0x10000
}


table switch_0_table {
	key {
		m.Ingress_switch_0_key exact
	}
	actions {
		switch_0_case
		switch_0_case_0
		switch_0_case_1
	}
	default_action switch_0_case_1 args none 
	size 0x10000
}


apply {
	rx m.psa_ingress_input_metadata_ingress_port
	mov m.psa_ingress_output_metadata_drop 0x0
	extract h.ethernet
	mov m.tmpMask h.ethernet.etherType
	and m.tmpMask 0xf00
	jmpeq MYIP_PARSE_IPV4 m.tmpMask 0x800
	jmpeq MYIP_PARSE_TCP h.ethernet.etherType 0xd00
	jmp MYIP_ACCEPT
	MYIP_PARSE_IPV4 :	extract h.ipv4
	mov m.tmpMask_0 h.ipv4.protocol
	and m.tmpMask_0 0xfc
	jmpeq MYIP_PARSE_TCP m.tmpMask_0 0x4
	jmp MYIP_ACCEPT
	MYIP_PARSE_TCP :	extract h.tcp
	MYIP_ACCEPT :	mov m.Ingress_tmp_0 0x10
	mov m.Ingress_switch_0_key 0x10
	jmpa LABEL_ACTION switch_0_case
	jmpa LABEL_ACTION_0 switch_0_case_0
	jmpa LABEL_ENDSWITCH switch_0_case_1
	jmp LABEL_ENDSWITCH
	LABEL_ACTION :	mov m.Ingress_tmp_0 0x1
	jmp LABEL_ENDSWITCH
	LABEL_ACTION_0 :	mov m.Ingress_tmp_0 0x2
	LABEL_ENDSWITCH :	mov m.Ingress_tbl_ethernet_srcAddr h.ethernet.srcAddr
	jmpa LABEL_ACTION_2 a1
	jmpa LABEL_ACTION_3 a2
	jmp LABEL_ENDSWITCH_0
	LABEL_ACTION_2 :	jmpneq LABEL_ENDSWITCH_0 m.Ingress_tmp_0 0x1
	table foo
	jmp LABEL_ENDSWITCH_0
	jmp LABEL_ENDSWITCH_0
	LABEL_ACTION_3 :	table bar
	LABEL_ENDSWITCH_0 :	jmpneq LABEL_DROP m.psa_ingress_output_metadata_drop 0x0
	emit h.ethernet
	tx m.psa_ingress_output_metadata_egress_port
	LABEL_DROP :	drop
}


